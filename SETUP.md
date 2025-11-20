# Setup Guide - PyTorch Bug Detector Demo

**✅ TESTED AND WORKING** - Last verified: 2025-11-20

This demo uses a **private analyzer repo** + **public test repo** to keep the analyzer code private.

## Quick Links

- **Quick Start:** [GITHUB_STEPS.md](GITHUB_STEPS.md) - 6-step checklist
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and fixes
- **This Guide:** Complete setup with explanations

---

## Important Notes

⚠️ **Ubuntu 22.04 Required:** The workflow uses `ubuntu-22.04` (not `ubuntu-latest`) because Souffle requires `libffi7`, which is only available in Ubuntu 22.04. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#error-depends-libffi7-but-it-is-not-installable) for details.

---

## Architecture

```
┌─────────────────────────────────┐
│  Private Repo (YOU create)      │
│  pytorch-analyzer                │
│  Contains: All analyzer code    │
└─────────────────────────────────┘
            ↓ cloned by workflow
┌─────────────────────────────────┐
│  Public Repo (this one)         │
│  pytorch-analyzer-demo           │
│  Contains: Test files + workflow│
└─────────────────────────────────┘
```

---

## Steps You Need to Do on GitHub

### Step 1: Create Private Analyzer Repo

1. Go to https://github.com/new
2. Create **private** repository named: `pytorch-analyzer`
3. **Don't** initialize with README (we'll push existing code)

### Step 2: Push Analyzer Code to Private Repo

On your local machine:

```bash
cd ~/pytorch-analyzer-demo  # The full analyzer code
git remote add origin https://github.com/YOUR_USERNAME/pytorch-analyzer.git
git push -u origin main
```

### Step 3: Create Personal Access Token

This token allows the workflow to clone your private repo.

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: `pytorch-analyzer-workflow`
4. Expiration: 90 days (or custom)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
6. Click "Generate token"
7. **COPY THE TOKEN** - you won't see it again!

### Step 4: Create Public Demo Repo

1. Go to https://github.com/new
2. Create **public** repository named: `pytorch-analyzer-demo`
3. **Don't** initialize with README

### Step 5: Push Public Demo Code

On your local machine:

```bash
cd ~/pytorch-analyzer-demo-public  # The minimal public repo
git init
git branch -m main
git add .
git commit -m "Initial commit: Public demo for PyTorch analyzer"
git remote add origin https://github.com/YOUR_USERNAME/pytorch-analyzer-demo.git
git push -u origin main
```

### Step 6: Add Secrets to Public Repo

In your **public** repo (pytorch-analyzer-demo):

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click "New repository secret"
3. Add two secrets:

**Secret 1:**
- Name: `ANALYZER_TOKEN`
- Value: [paste the token from Step 3]

**Secret 2:**
- Name: `ANALYZER_REPO`
- Value: `YOUR_USERNAME/pytorch-analyzer`

---

## Testing the Workflow

### Create Test PR

```bash
cd ~/pytorch-analyzer-demo-public

# Create test branch
git checkout -b test-bug-detection

# Modify test file (add a line to trigger change)
echo "" >> test_files/buggy_example.py

# Commit and push
git add .
git commit -m "Test bug detection"
git push -u origin test-bug-detection
```

### Open PR

1. Go to https://github.com/YOUR_USERNAME/pytorch-analyzer-demo
2. Click "Compare & pull request"
3. Create the PR
4. Watch the "Actions" tab

### Expected Results

- Action runs (~1-2 min)
- PR comment appears with bug table
- Download `bug_report.json` artifact from Actions tab

---

## What's Public vs Private

### Public (pytorch-analyzer-demo)
- ✅ Test Python files with bugs
- ✅ Workflow YAML file
- ✅ This setup guide
- ❌ NO analyzer code
- ❌ NO Souffle rules
- ❌ NO detection logic

### Private (pytorch-analyzer)
- ✅ All analyzer code (~300 files)
- ✅ Souffle Datalog rules
- ✅ Detection engine
- ✅ CFG builder
- ✅ Shape analyzer
- ✅ Everything proprietary

---

## Troubleshooting

### "Repository not found" error

- Check `ANALYZER_REPO` secret format: `username/repo` (no https://)
- Verify token has `repo` scope
- Ensure private repo name matches exactly

### "Permission denied" error

- Token might have expired
- Regenerate token with `repo` scope
- Update `ANALYZER_TOKEN` secret

### No bugs detected

- Check workflow logs in Actions tab
- Verify test file has actual PyTorch bugs
- Ensure analyzer code pushed to private repo

### Workflow not triggering

- PR must modify `.py` files
- Workflow file must be in `.github/workflows/`
- Check Actions tab for errors

---

## Security Notes

- ✅ Token is stored as encrypted secret
- ✅ Private repo never exposed in logs
- ✅ Analyzer code cloned temporarily, deleted after run
- ✅ Only analysis results are public (bug reports)

---

## Next Steps After Demo

Once validated:
1. Build Docker image for faster runs
2. Add caching for dependencies
3. Publish to GitHub Marketplace
4. Add configurable severity thresholds
