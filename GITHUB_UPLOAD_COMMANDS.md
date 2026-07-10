# GitHub Upload Commands

Replace `<your-github-username>` with your GitHub username.

## Option 1: Create Repo On GitHub Website First

1. Go to GitHub.
2. Create a new empty repository named:

```text
enterprise-llmops-ai-governance-platform
```

3. Do not add README, license, or `.gitignore` on GitHub because this project already has them.

Then run:

```powershell
cd C:\Users\ragha\Documents\Codex\2026-07-09\let\outputs\enterprise-llmops-ai-governance-platform-github-ready
git init
git add .
git commit -m "Initial commit: enterprise LLMOps AI governance platform"
git branch -M main
git remote add origin https://github.com/<your-github-username>/enterprise-llmops-ai-governance-platform.git
git push -u origin main
```

## Option 2: GitHub CLI

If GitHub CLI is installed and authenticated:

```powershell
cd C:\Users\ragha\Documents\Codex\2026-07-09\let\outputs\enterprise-llmops-ai-governance-platform-github-ready
git init
git add .
git commit -m "Initial commit: enterprise LLMOps AI governance platform"
git branch -M main
gh repo create enterprise-llmops-ai-governance-platform --public --source . --remote origin --push
```

## Recommended Before Upload

```powershell
.\scripts\run_offline_validation.ps1
```

Expected result:

```text
16 tests pass
governance gate approved
```
