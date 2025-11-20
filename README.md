# PyTorch Bug Detector - Demo

**✅ TESTED AND WORKING** - Successfully detecting PyTorch bugs on PRs!

This is a **public demo repository** for testing the PyTorch Bug Detector GitHub Action.

⚠️ **Note:** This repo contains only test files. The analyzer code is in a private repository.

## Documentation

- 📋 [GITHUB_STEPS.md](GITHUB_STEPS.md) - Quick 6-step setup guide
- 📖 [SETUP.md](SETUP.md) - Detailed setup instructions
- 🔧 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

## What This Demo Does

- Automatically analyzes PyTorch code in pull requests
- Detects gradient flow bugs (missing `backward()`, `zero_grad()`, etc.)
- Detects tensor shape mismatches
- Posts results as PR comments in LLM-friendly format

## Setup

See [SETUP.md](SETUP.md) for complete setup instructions.

## Quick Test

1. Fork this repo (or follow SETUP.md to create your own)
2. Add the required secrets (see SETUP.md)
3. Create a PR with modified `.py` files
4. See the analyzer run and report bugs

## Example Output

The action will post a PR comment like:

```
## 🔍 PyTorch Bug Detector Results

**Files analyzed:** 1
**Issues found:** 1 errors, 0 warnings

### Issues

| File | Line | Type | Severity | Message | Suggestion |
|------|------|------|----------|---------|------------|
| test_files/buggy_example.py | 30 | step_without_backward | 🔴 Error | optimizer.step() called without preceding loss.backward() | Add loss.backward() before optimizer.step() |
```

## Files

- `test_files/` - Sample buggy PyTorch code for testing
- `.github/workflows/pytorch-analyzer.yml` - GitHub Action workflow
- `SETUP.md` - Detailed setup instructions

## Architecture

This demo uses a two-repo architecture:
- **Private repo** (`pytorch-analyzer`) - Contains all analyzer code
- **Public repo** (this one) - Contains test files and workflow

The workflow clones the private repo during execution using a GitHub token.

## For LLM Tools

The bug report is available in two formats:
1. **PR Comment** - Markdown table (GitHub Copilot can see this)
2. **JSON Artifact** - Structured data (download from Actions tab for Claude Code)

## License

Demo files only - analyzer code is proprietary.
