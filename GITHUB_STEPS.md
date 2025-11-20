# GitHub Steps - Quick Reference

**You need to do 6 things on GitHub. Follow in order.**

---

## 1️⃣ Create Private Repo

**On GitHub:**
- Go to https://github.com/new
- Name: `pytorch-analyzer`
- Visibility: **Private** ⚠️
- Don't initialize

**On your machine:**
```bash
cd ~/pytorch-analyzer-demo
git remote add origin https://github.com/YOUR_USERNAME/pytorch-analyzer.git
git push -u origin main
```

✅ **Checkpoint:** Private repo should have ~300 files

---

## 2️⃣ Create Personal Access Token

**On GitHub:**
- Go to https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Name: `pytorch-analyzer-workflow`
- Expiration: 90 days
- Scopes: Check ✅ `repo`
- Generate token
- **COPY THE TOKEN** 📋

✅ **Checkpoint:** Token copied (looks like `ghp_xxxxxxxxxxxx`)

---

## 3️⃣ Create Public Repo

**On GitHub:**
- Go to https://github.com/new
- Name: `pytorch-analyzer-demo`
- Visibility: **Public** 🌍
- Don't initialize

**On your machine:**
```bash
cd ~/pytorch-analyzer-demo-public
git remote add origin https://github.com/YOUR_USERNAME/pytorch-analyzer-demo.git
git push -u origin main
```

✅ **Checkpoint:** Public repo should have 5 files

---

## 4️⃣ Add Secrets to Public Repo

**On GitHub (in public repo):**
- Go to Settings → Secrets and variables → Actions
- Click "New repository secret"

**Add Secret #1:**
- Name: `ANALYZER_TOKEN`
- Value: [paste token from step 2]

**Add Secret #2:**
- Name: `ANALYZER_REPO`
- Value: `YOUR_USERNAME/pytorch-analyzer`
  (Replace YOUR_USERNAME with your actual username)

✅ **Checkpoint:** Should see 2 secrets listed

---

## 5️⃣ Test the Workflow

**On your machine:**
```bash
cd ~/pytorch-analyzer-demo-public
git checkout -b test-bugs
echo "" >> test_files/buggy_example.py
git add .
git commit -m "Test analyzer"
git push -u origin test-bugs
```

✅ **Checkpoint:** Branch pushed

---

## 6️⃣ Open PR and Watch

**On GitHub (in public repo):**
- Click "Compare & pull request" button
- Create the PR
- Go to "Actions" tab
- Watch the workflow run (~1-2 min)
- Check PR for comment with bug report

✅ **Success:** PR comment shows detected bugs!

---

## Summary

| What | Where | Status |
|------|-------|--------|
| Private repo created | `pytorch-analyzer` | ⬜ |
| Token created | Settings → Tokens | ⬜ |
| Public repo created | `pytorch-analyzer-demo` | ⬜ |
| Secrets added | Public repo settings | ⬜ |
| Test branch pushed | Public repo | ⬜ |
| PR created | Public repo | ⬜ |

---

## If Something Goes Wrong

**"Repository not found"**
- Check `ANALYZER_REPO` format: `username/repo` (no https)
- Verify private repo exists and name matches

**"Permission denied"**
- Check token has `repo` scope
- Regenerate token if needed

**Workflow doesn't run**
- Ensure workflow file is in `.github/workflows/`
- PR must change `.py` files

See [SETUP.md](SETUP.md) for detailed troubleshooting.
