# Security Best Practices for Isabella

## 🚨 CRITICAL: Never Commit Secrets to GitHub

API keys, tokens, and credentials are **NEVER** meant to be committed to version control. Ever.

### What Happened
Your OpenRouter API key was accidentally exposed in `GOOGLE_DRIVE_SETUP.md` documentation.

**Actions Taken:**
1. ✅ Removed the exposed key from the documentation file
2. ✅ Updated `.gitignore` to prevent future leaks
3. ✅ Rewrote entire git history using `git-filter-repo` to remove the key from all commits
4. ✅ Force-pushed cleaned history to GitHub

### What You MUST Do Now
1. **IMMEDIATELY rotate your OpenRouter API key** at https://openrouter.io/account/api-keys
   - Generate a new key
   - Delete the old exposed key
   - Update Railway environment variable with the new key

2. **Check GitHub Dependabot/Security alerts** - They may have flagged this

3. **Follow the security guidelines below**

---

## Secrets Management Rules

### ✅ DO
- Store all secrets in **environment variables** ONLY
- Use `.env` files locally (added to `.gitignore`)
- On Railway: Use the "Variables" tab to add secrets
- Document what env vars are needed (WITHOUT values)
- Use placeholders like `<your-key-here>` in docs

### ❌ DON'T
- Hardcode API keys in code
- Include real secrets in documentation
- Commit `.env` files
- Share keys in comments or examples
- Use keys in test data

---

## Current Setup

### Required Environment Variables
These MUST be set on Railway:

| Variable | Purpose | Where to Get |
|----------|---------|--------------|
| `GOOGLE_OAUTH_TOKEN_JSON` | Google Drive access | [Google Cloud Console](https://console.cloud.google.com/) |
| `OPENROUTER_API_KEY` | AI model access | [OpenRouter](https://openrouter.io/account/api-keys) |

### Local Development (.env file)
```bash
# Create .env file (NEVER commit this!)
GOOGLE_OAUTH_TOKEN_JSON={"type": "authorized_user", ...}
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

Then in code:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file
api_key = os.environ.get("OPENROUTER_API_KEY")
```

### Production (Railway)
1. Go to your Railway project
2. Click "Variables"
3. Add both environment variables
4. Deploy (Railway automatically applies them)

---

## .gitignore Updates

Your `.gitignore` has been updated to include:
```
.env
.env.local
.env*.local
client_secret.json
token.json
*.key
*.pem
*.secrets
credentials.json
```

This prevents accidentally committing secrets.

---

## If Secrets Are Accidentally Committed

### Immediate Actions
1. **Don't panic, but act fast**
2. Rotate the exposed secrets immediately
3. Verify if anyone has access (GitHub shows who accessed the commit)
4. Rewrite git history using `git-filter-repo` (what we just did)
5. Force-push to overwrite public history

### Tools to Use
```bash
# 1. Install git-filter-repo
pip install git-filter-repo

# 2. Create expressions file with the secret
echo "my-exposed-secret-key" > redact.txt

# 3. Rewrite history
git-filter-repo --replace-text redact.txt --force

# 4. Restore remote and push
git remote add origin https://github.com/yourusername/repo.git
git push --force origin main
```

---

## Testing Your Setup

**Check that secrets are loaded correctly:**

```bash
# The /diagnose endpoint shows:
curl http://localhost:8000/diagnose

# Should show:
{
  "status": "ok",
  "google_auth_configured": true,
  "openrouter_configured": true,
  "version": "4.0.0"
}
```

---

## References
- [GitHub Secret Scanning](https://github.com/features/security/secret-scanning)
- [git-filter-repo Manual](https://github.com/newren/git-filter-repo/blob/main/docs/man1/git-filter-repo.1.md)
- [OpenRouter API Keys](https://openrouter.io/account/api-keys)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Summary

**Your repository is now secure:**
- ✅ Exposed key removed from all commits
- ✅ History rewritten and force-pushed
- ✅ .gitignore enhanced
- ✅ Documentation updated to never show real secrets

**Action required from you:**
1. Rotate your OpenRouter API key NOW
2. Update Railway environment variables with the new key
3. Keep this document as reference for future development

