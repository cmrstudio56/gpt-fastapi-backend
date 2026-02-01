# 🔧 Google Drive Setup Guide for Custom GPT

## Problem
Your Custom GPT is showing test/sample files instead of your actual Google Drive files.

## Root Cause
The `GOOGLE_OAUTH_TOKEN_JSON` environment variable is **NOT SET** on Railway, so the API cannot authenticate with Google Drive.

---

## ✅ Solution (3 Steps)

### Step 1: Check Your Token
You need to get your **Google OAuth token** from `token.json` file.

⚠️ **SECURITY NOTE:** Never commit API keys, tokens, or secrets to GitHub. Keep credentials only in environment variables.

```bash
# On your local machine, find token.json
cat c:\Users\os_ol\Documents\fastapi-gpt\token.json
```

This file contains your Google Drive credentials. It should look like:
```json
{
  "type": "authorized_user",
  "client_id": "...",
  "client_secret": "...",
  "refresh_token": "...",
  "access_token": "..."
}
```

### Step 2: Copy the JSON Content
1. Open `token.json` file
2. Select ALL content (Ctrl+A)
3. Copy it (Ctrl+C)

### Step 3: Add to Railway
1. Go to: https://railway.app/project/...
2. Click **Variables** (or Settings → Variables)
3. Click **New Variable**
4. **Name**: `GOOGLE_OAUTH_TOKEN_JSON`
5. **Value**: Paste the ENTIRE `token.json` content (as a JSON string, not formatted)
6. Click **Save**
7. Railway will **automatically redeploy** in 1-2 minutes

---

## ✔️ Verify It Works

### Test the Health Check
```bash
curl https://web-production-99e37.up.railway.app/
```

Should return:
```json
{
  "status": "ok",
  "message": "API is running",
  "google_drive_ready": true,
  "openrouter_configured": true,
  "env_vars": {
    "GOOGLE_OAUTH_TOKEN_JSON": "✓ SET",
    "OPENROUTER_API_KEY": "✓ SET"
  }
}
```

### Diagnose Full Status
```bash
curl https://web-production-99e37.up.railway.app/diagnose
```

This will show:
- ✓ or ✗ for each component
- Your actual Google Drive folder contents
- Storage quota usage
- Any errors

### List Your Real Drive Files
```bash
curl https://web-production-99e37.up.railway.app/list?path=default
```

Should show your actual files, not test samples!

---

## 📝 Important File Locations

| File | Purpose | Location |
|------|---------|----------|
| `token.json` | Google Drive auth token | Local: `c:\Users\os_ol\Documents\fastapi-gpt\token.json` |
| `fastapi openrouter .txt` | OpenRouter API key | Local: project folder |
| Env vars | Credentials on Railway | Railway Dashboard → Variables |

---

## 🔑 Environment Variables Needed

Set these on **Railway Dashboard → Variables**:

| Name | Value | Source |
|------|-------|--------|
| `GOOGLE_OAUTH_TOKEN_JSON` | Content of `token.json` | Local file |
| `OPENROUTER_API_KEY` | `sk-or-v1-...` | From `fastapi openrouter .txt` |

---

## 🚀 Using with Custom GPT

Once Google Drive is connected:

1. **List your files**: `GET /list?path=default`
2. **Create a file**: `POST /write` with your project name
3. **Read from Drive**: `GET /read?title=filename&project=myproject`
4. **Summarize files**: `POST /summarize` with OpenRouter AI

---

## ❌ If Still Not Working

### Check Railway Logs
1. Go to Railway dashboard
2. Click **Deployments**
3. Find the latest deployment
4. Click **Logs** tab
5. Look for error messages about Google Drive

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'requests'`
- **Fix**: Already in requirements.txt, will auto-install on Railway

**Issue**: `Failed to load credentials from env`
- **Fix**: JSON might be malformed. Copy the ENTIRE token.json exactly

**Issue**: `"File 'title' not found"`
- **Fix**: Check files exist in your project folder: `GET /list?path=projectname`

**Issue**: See only test/sample files
- **Fix**: Google Drive NOT connected. Complete Steps 1-3 above.

---

## 📋 Quick Checklist

- [ ] Found `token.json` file locally
- [ ] Copied entire JSON content
- [ ] Added `GOOGLE_OAUTH_TOKEN_JSON` variable to Railway
- [ ] Railway auto-deployed (wait 1-2 min)
- [ ] Tested `/diagnose` endpoint
- [ ] `/list` shows your real files
- [ ] Custom GPT now connected to real Google Drive

---

## 🆘 Need Help?

Try the diagnostic endpoint to pinpoint the issue:
```bash
curl https://web-production-99e37.up.railway.app/diagnose
```

This shows exactly what's configured and what's missing.
