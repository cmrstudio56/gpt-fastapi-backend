# Isabella - AI-Powered Google Drive Manager

**Version:** 4.2.0  
**Status:** ✅ Production Ready  
**Endpoints:** 22 Total  
**Deployment:** Railway (Auto-deployed from GitHub)

---

## 🎯 What is Isabella?

Isabella is a **full-featured Google Drive management API** with AI capabilities. She handles:
- Complete file organization (create, move, copy, delete)
- Folder management and storage analytics
- File recovery (trash system)
- Sharing and permissions
- AI-powered text summarization
- Universal file type support (PDF, DOCX, EPUB, images, etc.)

**It's like having a smart assistant for your Google Drive!** 🤖

---

## 🚀 Quick Start

### Live API
```
https://web-production-99e37.up.railway.app
Swagger UI: https://web-production-99e37.up.railway.app/docs
```

### Check Status
```bash
curl https://web-production-99e37.up.railway.app/
```

### See All Your Files
```bash
curl https://web-production-99e37.up.railway.app/list-all
```

---

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** ⭐ Start here! Essential commands
- **[PHASE1_FILE_MANAGEMENT.md](PHASE1_FILE_MANAGEMENT.md)** - Delete, create, move, copy, download
- **[PHASE2_ADVANCED_OPERATIONS.md](PHASE2_ADVANCED_OPERATIONS.md)** - Trash, restore, stats, metadata, share
- **[DEPLOYMENT_v4.2.0.md](DEPLOYMENT_v4.2.0.md)** - Full deployment guide
- **[BROWSE_DRIVE.md](BROWSE_DRIVE.md)** - All listing/browsing endpoints
- **[SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md)** - API key safety
- **[ISABELLA_SKILLS.md](ISABELLA_SKILLS.md)** - Skills registry
- **[ISABELLA_ARCHITECTURE.md](ISABELLA_ARCHITECTURE.md)** - System design

---

## ✨ Features

### 📂 Browse Drive (5 endpoints)
- `/list-all` - See all root items
- `/list?path=X` - Browse specific folder
- `/list-detailed?path=X` - With metadata
- `/list-recursive?path=X` - Tree structure
- `/search?query=X` - Search anywhere

### 📝 File Operations (5 endpoints)
- `/write` - Create files
- `/read` - Read content
- `/append` - Add to files
- `/delete` - Remove files
- `/download` - Export content

### 🗂️ Folder Management (4 endpoints)
- `/create-folder` - New folders
- `/move` - Reorganize
- `/copy` - Duplicate files
- `/delete-folder` - Remove folders

### 🔄 Advanced (6 endpoints)
- `/trash` - View deleted items
- `/restore` - Recover files
- `/empty-trash` - Permanent delete
- `/folder-stats` - Storage info
- `/metadata` - File details
- `/share` - Share with others

### 🤖 AI Features (2 endpoints)
- `/summarize` - AI-powered summarization (6 models)
- `/models` - List available AI models

### 🔧 System (2 endpoints)
- `/` - Health check
- `/diagnose` - Full diagnostics

---

## 🎮 Usage Examples

### Create Organized Structure
```bash
# Create folders
curl -X POST "https://...up.railway.app/create-folder?folder_name=Books&parent_path=default"
curl -X POST "https://...up.railway.app/create-folder?folder_name=Projects&parent_path=default"
curl -X POST "https://...up.railway.app/create-folder?folder_name=Archive&parent_path=default"
```

### Organize Files
```bash
# Move file to organize
curl -X POST "https://...up.railway.app/move?title=myfile&from_project=default&to_project=Books"
```

### Backup & Clean
```bash
# Backup important file
curl -X POST "https://...up.railway.app/copy?title=important&project=default&new_name=important_backup"

# Delete and archive later
curl -X DELETE "https://...up.railway.app/delete?title=temporary&project=default"
```

### Monitor Storage
```bash
# Check folder size
curl "https://...up.railway.app/folder-stats?path=Books"
```

### Summarize Documents
```bash
# AI-powered summary
curl -X POST https://...up.railway.app/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "title": "long_document",
    "project": "default",
    "model": "claude-3-5-sonnet"
  }'
```

---

## 🔐 Setup Requirements

### Environment Variables (Set on Railway)
```
GOOGLE_OAUTH_TOKEN_JSON = (your Google OAuth token)
OPENROUTER_API_KEY = (your OpenRouter API key - MUST BE ROTATED)
```

### Get Google OAuth Token
1. Go to Google Cloud Console
2. Create OAuth credentials
3. Run `python -m google_auth_oauthlib.flow` locally
4. Copy entire `token.json` to Railway as env var

### Get OpenRouter API Key
1. Visit https://openrouter.io/account/api-keys
2. Generate new key
3. Add to Railway `OPENROUTER_API_KEY` env var

⚠️ **IMPORTANT:** Your old OpenRouter key was exposed. Generate a new one and update Railway!

---

## 🏗️ Architecture

**Skill 1: Google Drive Manager** (Active ✅)
- Complete file/folder management
- AI summarization
- Full API coverage

**Skill 2: Story Writer** (Planned)
- Creative writing assistance
- Character development
- Scene generation

**Skill 3: Tutor** (Planned)
- Educational content
- Q&A system
- Assessment

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Endpoints | 22 |
| File Types Supported | All (PDF, DOCX, EPUB, images, etc.) |
| Max Items Per Request | 1000 |
| AI Models | 6 (Claude, GPT-4, Llama, Mistral) |
| Deployment | Railway (Auto-git-deploy) |
| Version | 4.2.0 |

---

## 🐛 Troubleshooting

### API Returns "Google Drive not initialized"
→ Check `GOOGLE_OAUTH_TOKEN_JSON` is set on Railway

### Can only see TXT files
→ FIXED in v4.1.0 - now shows all file types

### Want API key safety guide
→ Read [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md)

### Full system check
→ Run: `curl https://...up.railway.app/diagnose`

---

## 📝 Version History

- **v4.2.0** - Phase 2: Advanced operations (trash, restore, stats, metadata, share)
- **v4.1.0** - Phase 1: File management (delete, create-folder, move, copy, download)
- **v4.0.0** - Removed book management, full Google Drive focus
- **v3.6.0** - Multi-book management with OpenRouter AI

---

## 🚀 Deployment

Automatic deployment on push to `main` branch:
1. Code pushed to GitHub
2. Railway detects changes
3. Auto-builds and deploys
4. Live in ~5 minutes

See [DEPLOYMENT_v4.2.0.md](DEPLOYMENT_v4.2.0.md) for details.

---

## 📞 Support

- **Quick Help:** [QUICK_START.md](QUICK_START.md)
- **Features:** [PHASE1_FILE_MANAGEMENT.md](PHASE1_FILE_MANAGEMENT.md) & [PHASE2_ADVANCED_OPERATIONS.md](PHASE2_ADVANCED_OPERATIONS.md)
- **System Info:** [ISABELLA_ARCHITECTURE.md](ISABELLA_ARCHITECTURE.md)
- **Security:** [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md)

---

## ✅ Status

- ✅ Production ready
- ✅ All 22 endpoints working
- ✅ Error handling complete
- ✅ Security reviewed
- ✅ Deployed to Railway
- ✅ Documentation complete

**Your Google Drive is now fully manageable through Isabella!** 🎉
