# Troubleshooting Guide - PyTorch Bug Detector GitHub Action

**Last Updated:** 2025-11-20

This guide covers common issues encountered during setup and how to fix them.

---

## Table of Contents

1. [Souffle Installation Issues](#souffle-installation-issues)
2. [Authentication & Secrets Issues](#authentication--secrets-issues)
3. [Workflow Not Running](#workflow-not-running)
4. [Analysis Issues](#analysis-issues)
5. [Performance Issues](#performance-issues)

---

## Souffle Installation Issues

### ❌ Error: "Unable to locate package souffle"

**Full Error:**
```
E: Unable to locate package souffle
Error: Process completed with exit code 100
```

**Cause:** Ubuntu's default repositories don't include Souffle.

**Solution:** Use the official Souffle PPA (already included in our workflow):

```yaml
- name: Install Souffle
  run: |
    sudo apt-get update
    sudo apt-get install -y wget software-properties-common
    sudo mkdir -p /etc/apt/keyrings
    wget -qO- "https://souffle-lang.github.io/ppa/souffle-key.public" | sudo tee /etc/apt/keyrings/souffle-archive-keyring.gpg
    echo "deb [signed-by=/etc/apt/keyrings/souffle-archive-keyring.gpg] https://souffle-lang.github.io/ppa/ubuntu/ stable main" | sudo tee /etc/apt/sources.list.d/souffle.list
    sudo apt-get update
    sudo apt-get install -y souffle
```

**Status:** ✅ Fixed in current workflow

---

### ❌ Error: "Depends: libffi7 but it is not installable"

**Full Error:**
```
The following packages have unmet dependencies:
 souffle : Depends: libffi7 (>= 3.3~20180313) but it is not installable
E: Unable to correct problems, you have held broken packages.
```

**Cause:** Ubuntu 24.04 (ubuntu-latest) has `libffi8`, but Souffle PPA requires `libffi7`.

**Solution:** Use Ubuntu 22.04 instead:

```yaml
jobs:
  analyze:
    runs-on: ubuntu-22.04  # NOT ubuntu-latest!
```

**Status:** ✅ Fixed in current workflow

**Why This Matters:**
- `ubuntu-latest` = Ubuntu 24.04 (as of Nov 2024)
- Ubuntu 24.04 ships with `libffi8`
- Souffle PPA is built for Ubuntu 22.04 with `libffi7`
- Must explicitly specify `ubuntu-22.04` until Souffle PPA updates

---

## Authentication & Secrets Issues

### ❌ Error: "Repository not found"

**Full Error:**
```
fatal: repository 'https://github.com/username/pytorch-analyzer.git/' not found
```

**Possible Causes:**

1. **Wrong repository name in secret**
   - Check `ANALYZER_REPO` secret
   - Should be: `username/repo` (NOT `https://github.com/username/repo`)
   - Example: `telos27/pytorch-analyzer` ✅
   - NOT: `https://github.com/telos27/pytorch-analyzer` ❌

2. **Private repo doesn't exist**
   - Verify the private repo exists at the URL
   - Check spelling and capitalization

3. **Token doesn't have access**
   - Token must have `repo` scope
   - Token must not be expired

**How to Fix:**

1. Go to your public repo → Settings → Secrets and variables → Actions
2. Edit `ANALYZER_REPO` secret
3. Ensure format is: `username/repo-name`
4. Save

---

### ❌ Error: "Permission denied" or "403 Forbidden"

**Possible Causes:**

1. **Token expired**
   - Personal access tokens expire (default: 90 days)

2. **Token missing `repo` scope**
   - Token needs full `repo` access to clone private repositories

3. **Wrong token in secret**
   - Copy-paste error when adding token

**How to Fix:**

1. Create new token:
   - Go to https://github.com/settings/tokens
   - Generate new token (classic)
   - Select `repo` scope
   - Copy the token

2. Update secret:
   - Public repo → Settings → Secrets → Actions
   - Edit `ANALYZER_TOKEN`
   - Paste new token
   - Save

---

### ❌ Error: "Secret ANALYZER_TOKEN is not available"

**Cause:** Secret not added to repository.

**Solution:**

1. Go to public repo → Settings → Secrets and variables → Actions
2. Add both required secrets:
   - `ANALYZER_TOKEN` = your personal access token
   - `ANALYZER_REPO` = `username/private-repo-name`

---

## Workflow Not Running

### Issue: Workflow doesn't trigger on PR

**Possible Causes:**

1. **No Python files changed**
   - Workflow only runs when `.py` files are modified
   - Check the `paths:` filter in workflow

2. **Workflow file not in correct location**
   - Must be in `.github/workflows/` directory
   - Must have `.yml` or `.yaml` extension

3. **Workflow disabled**
   - Check Actions tab → Workflows → ensure not disabled

**How to Fix:**

Ensure PR modifies at least one `.py` file:
```bash
# Add a comment or blank line to trigger
echo "" >> test_files/buggy_example.py
git add .
git commit -m "Trigger workflow"
git push
```

---

### Issue: Workflow shows "Queued" but never runs

**Cause:** GitHub Actions quota exceeded (rare for public repos).

**Solution:**
- Public repos have unlimited minutes
- Check Settings → Billing if private repo

---

## Analysis Issues

### Issue: No bugs detected when bugs exist

**Possible Causes:**

1. **Analyzer code not up to date**
   - Private repo might be out of sync
   - Push latest analyzer code to private repo

2. **File path issues**
   - Workflow analyzes files from public repo root
   - Ensure paths are correct in workflow

**Debug Steps:**

1. Check workflow logs in Actions tab
2. Look for "Analyzing: filename.py" messages
3. Verify files are being found and analyzed

---

### Issue: "Cannot open fact file" errors

**Cause:** Missing fact groups in `bug_detection_engine.py`.

**Solution:** This is an analyzer code issue. Ensure all fact types are registered in the private repo's `bug_detection_engine.py`.

---

## Performance Issues

### Issue: Workflow takes >5 minutes

**Current Times:**
- First run: ~1-2 minutes
- Cached runs: ~1-2 minutes (similar, no significant cache benefit yet)

**If slower:**

1. **Add caching for Souffle binary:**

```yaml
- name: Cache Souffle
  uses: actions/cache@v4
  with:
    path: /usr/bin/souffle
    key: souffle-${{ runner.os }}-22.04
```

2. **Add caching for Python dependencies:**

```yaml
- name: Cache Python packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ hashFiles('analyzer/requirements.txt') }}
```

---

## Testing & Debugging

### How to Test Locally

You can't fully test the workflow locally (requires GitHub infrastructure), but you can test the analyzer:

```bash
# Clone both repos
git clone https://github.com/username/pytorch-analyzer.git
git clone https://github.com/username/pytorch-analyzer-demo.git

# Test analyzer on demo files
cd pytorch-analyzer
python cli_bug_detector.py ../pytorch-analyzer-demo/test_files/buggy_example.py --json
```

### How to Debug Workflow Failures

1. **View detailed logs:**
   - PR → Actions tab → Click failed run
   - Expand each step to see full output

2. **Check for step failures:**
   - Red X = failed step
   - Click to see error message

3. **Common error locations:**
   - "Install Souffle" - dependency issues
   - "Clone private analyzer repo" - authentication issues
   - "Run PyTorch Bug Detector" - analyzer code issues

---

## Getting Help

If you encounter an issue not covered here:

1. **Check workflow logs** in the Actions tab
2. **Copy the full error message**
3. **Check if it's a known limitation** in the analyzer
4. **Create an issue** with:
   - Full error message
   - Workflow run link
   - Steps to reproduce

---

## Summary of Current Configuration

**Working Configuration (as of 2025-11-20):**

```yaml
runs-on: ubuntu-22.04  # Required for libffi7

steps:
  # Install Souffle from official PPA
  - name: Install Souffle
    run: |
      sudo apt-get update
      sudo apt-get install -y wget software-properties-common
      sudo mkdir -p /etc/apt/keyrings
      wget -qO- "https://souffle-lang.github.io/ppa/souffle-key.public" | sudo tee /etc/apt/keyrings/souffle-archive-keyring.gpg
      echo "deb [signed-by=/etc/apt/keyrings/souffle-archive-keyring.gpg] https://souffle-lang.github.io/ppa/ubuntu/ stable main" | sudo tee /etc/apt/sources.list.d/souffle.list
      sudo apt-get update
      sudo apt-get install -y souffle

  # Clone private repo with token
  - name: Clone private analyzer repo
    run: |
      git clone https://x-access-token:${{ secrets.ANALYZER_TOKEN }}@github.com/${{ secrets.ANALYZER_REPO }}.git analyzer
```

**Required Secrets:**
- `ANALYZER_TOKEN` - Personal access token with `repo` scope
- `ANALYZER_REPO` - Format: `username/repo-name` (no https)

---

**Need more help?** Check the detailed setup guide in [SETUP.md](SETUP.md) or [GITHUB_STEPS.md](GITHUB_STEPS.md).
