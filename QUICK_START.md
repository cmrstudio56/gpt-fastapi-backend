# 🚀 Isabella v4.2.0 Quick Start Guide

## API Endpoint
```
https://web-production-99e37.up.railway.app
```

Swagger UI: https://web-production-99e37.up.railway.app/docs

---

## Essential Commands

### 1️⃣ Check API Status
```bash
curl https://web-production-99e37.up.railway.app/
```

### 2️⃣ See All Your Drive Files
```bash
curl https://web-production-99e37.up.railway.app/list-all
```

### 3️⃣ List Specific Folder
```bash
curl "https://web-production-99e37.up.railway.app/list?path=default"
```

### 4️⃣ Create New File
```bash
curl -X POST https://web-production-99e37.up.railway.app/write \
  -H "Content-Type: application/json" \
  -d '{
    "title": "my_file",
    "content": "Hello, world!",
    "project": "default"
  }'
```

### 5️⃣ Read File
```bash
curl "https://web-production-99e37.up.railway.app/read?title=my_file&project=default"
```

### 6️⃣ Create Folder
```bash
curl -X POST "https://web-production-99e37.up.railway.app/create-folder?folder_name=MyFolder&parent_path=default"
```

### 7️⃣ Move File
```bash
curl -X POST "https://web-production-99e37.up.railway.app/move?title=my_file&from_project=default&to_project=MyFolder"
```

### 8️⃣ Copy File
```bash
curl -X POST "https://web-production-99e37.up.railway.app/copy?title=my_file&project=default&new_name=my_file_copy"
```

### 9️⃣ Delete File
```bash
curl -X DELETE "https://web-production-99e37.up.railway.app/delete?title=my_file&project=default"
```

### 🔟 Get Folder Stats
```bash
curl "https://web-production-99e37.up.railway.app/folder-stats?path=default"
```

---

## File Management Workflow

```
1. CREATE STRUCTURE
   └─ POST /create-folder → Create "Projects"
   
2. ADD FILES
   ├─ POST /write → Create file in "Projects"
   └─ POST /write → Create another file
   
3. ORGANIZE
   ├─ POST /create-folder → Create "Archive"
   └─ POST /move → Move old files to "Archive"
   
4. MONITOR
   └─ GET /folder-stats → Check size
   
5. CLEAN UP (When ready)
   └─ DELETE /empty-trash → Permanently delete
```

---

## Common Tasks

### Task: Backup Important File
```bash
# Copy before deleting
curl -X POST "https://web-production-99e37.up.railway.app/copy?title=important&project=default&new_name=important_backup"

# Move original to Archive
curl -X POST "https://web-production-99e37.up.railway.app/move?title=important&from_project=default&to_project=Archive"
```

### Task: Organize Drive
```bash
# Create folders
curl -X POST "https://web-production-99e37.up.railway.app/create-folder?folder_name=Books&parent_path=default"
curl -X POST "https://web-production-99e37.up.railway.app/create-folder?folder_name=Projects&parent_path=default"
curl -X POST "https://web-production-99e37.up.railway.app/create-folder?folder_name=Archive&parent_path=default"

# List to verify
curl "https://web-production-99e37.up.railway.app/list?path=default"
```

### Task: Find & Read File
```bash
# Search for file
curl "https://web-production-99e37.up.railway.app/search?query=novel"

# Read it
curl "https://web-production-99e37.up.railway.app/read?title=novel&project=default"
```

### Task: Summarize Document
```bash
curl -X POST https://web-production-99e37.up.railway.app/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "title": "long_document",
    "project": "default",
    "model": "claude-3-5-sonnet",
    "max_length": 300
  }'
```

### Task: Share File
```bash
curl -X POST "https://web-production-99e37.up.railway.app/share?title=my_file&project=default&email=friend@gmail.com&role=reader"
```

### Task: Recover Deleted File
```bash
# List trash
curl "https://web-production-99e37.up.railway.app/trash"

# Restore (use file_id from trash list)
curl -X POST "https://web-production-99e37.up.railway.app/restore?file_id=abc123&restore_to_project=default"
```

---

## 22 Endpoints Overview

```
BROWSE DRIVE
├─ GET  /list-all                    → All root items
├─ GET  /list?path=X                 → Specific folder
├─ GET  /list-detailed?path=X        → With metadata
├─ GET  /list-recursive?path=X       → Tree structure
└─ GET  /search?query=X              → Find files

FILE I/O
├─ POST /write                       → Create file
├─ GET  /read?title=X                → Read file
└─ POST /append                      → Add content

FILE OPERATIONS
├─ DELETE /delete?title=X            → Remove file
├─ POST /create-folder               → New folder
├─ POST /move                        → Reorganize
├─ POST /copy                        → Duplicate
└─ GET  /download?title=X            → Export

ADVANCED
├─ DELETE /delete-folder             → Remove folder
├─ GET /trash                        → View deleted
├─ POST /restore                     → Recover
├─ DELETE /empty-trash               → Permanent delete
├─ GET /folder-stats?path=X          → Statistics
├─ GET /metadata?title=X             → Details
└─ POST /share                       → Share file

AI
├─ POST /summarize                   → AI summary
└─ GET  /models                      → List models

SYSTEM
├─ GET  /                            → Health check
└─ GET  /diagnose                    → Full diagnostics
```

---

## Parameters Reference

### Common Parameters
```
title      = File name (without .txt)
project    = Folder name (default: "default")
path       = Folder path
query      = Search term
email      = Email for sharing
role       = "reader" | "writer" | "owner"
file_id    = File ID from trash/metadata
folder_name = New folder name
new_name   = Custom copy name
max_items  = Results limit (default: 50)
```

### Models for Summarization
```
"claude-3-5-sonnet"   ← Best for text
"claude-3-opus"
"gpt-4o"
"gpt-4-turbo"
"llama-2"
"mistral"
```

---

## Error Responses

All errors follow this format:
```json
{
  "status": "error",
  "message": "What went wrong"
}
```

### Common Errors & Solutions

| Error | Solution |
|-------|----------|
| `Google Drive service not initialized` | Check GOOGLE_OAUTH_TOKEN_JSON env var on Railway |
| `File not found` | Verify file name and project folder exist |
| `Failed to create folder` | Check parent folder path is correct |
| `Folder not found` | Use `/list` to see available folders |

---

## Pro Tips

1. **Use `/diagnose`** to check system status before troubleshooting
2. **Use `/folder-stats`** to monitor storage usage
3. **Use `/trash` before `/empty-trash`** to see what will be deleted
4. **Use `/metadata`** to get sharing links and file info
5. **Use `/search`** for large drives instead of `/list` (faster)
6. **Combine `/list-recursive`** with a small folder to see structure

---

## API Response Codes

- `200` - Success ✅
- `400` - Bad request (check parameters)
- `404` - File/folder not found
- `500` - Server error (check `/diagnose`)

---

## Need Help?

1. Check `/diagnose` endpoint
2. Read [PHASE1_FILE_MANAGEMENT.md](PHASE1_FILE_MANAGEMENT.md)
3. Read [PHASE2_ADVANCED_OPERATIONS.md](PHASE2_ADVANCED_OPERATIONS.md)
4. Read [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md)

---

**Isabella v4.2.0 - Your Complete Google Drive Manager** 🚀

