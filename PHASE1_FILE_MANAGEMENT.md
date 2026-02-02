# Phase 1 File Management Operations

## ✅ Now Available (v4.1.0)

Isabella now has **5 powerful file management endpoints** for complete Drive control!

---

## 🗑️ DELETE FILE

**Remove a file permanently**

```bash
curl -X DELETE "http://localhost:8000/delete?title=myfile&project=default"
```

**Response:**
```json
{
  "status": "success",
  "message": "File 'myfile' deleted from project 'default'"
}
```

---

## 📁 CREATE FOLDER

**Create a new folder inside an existing folder**

```bash
# Create folder in default project
curl -X POST "http://localhost:8000/create-folder?folder_name=MyNewFolder&parent_path=default"

# Create nested folder
curl -X POST "http://localhost:8000/create-folder?folder_name=SubFolder&parent_path=Books"
```

**Response:**
```json
{
  "status": "success",
  "message": "Folder 'MyNewFolder' created",
  "folder_id": "abc123xyz",
  "folder_name": "MyNewFolder"
}
```

---

## ↔️ MOVE FILE

**Move file from one folder to another**

```bash
# Move from "Books" to "Archive"
curl -X POST "http://localhost:8000/move?title=novel&from_project=Books&to_project=Archive"
```

**Response:**
```json
{
  "status": "success",
  "message": "File 'novel' moved from 'Books' to 'Archive'"
}
```

---

## 📋 COPY FILE

**Duplicate a file (with optional new name)**

```bash
# Copy with automatic "_copy" suffix
curl -X POST "http://localhost:8000/copy?title=document&project=default"

# Copy with custom name
curl -X POST "http://localhost:8000/copy?title=document&project=default&new_name=document_backup"
```

**Response:**
```json
{
  "status": "success",
  "message": "File copied as 'document_copy'",
  "original": "document",
  "copy_name": "document_copy",
  "copy_id": "def456uvw"
}
```

---

## ⬇️ DOWNLOAD FILE

**Export file content as raw text**

```bash
curl "http://localhost:8000/download?title=myfile&project=default"
```

**Response:**
```json
{
  "status": "success",
  "filename": "myfile.txt",
  "project": "default",
  "content": "This is the file content...",
  "content_length": 1234
}
```

---

## Complete Endpoint Reference

| Operation | Method | Endpoint | Purpose |
|-----------|--------|----------|---------|
| Delete | DELETE | `/delete?title=X&project=Y` | Remove file |
| Create Folder | POST | `/create-folder?folder_name=X&parent_path=Y` | New folder |
| Move | POST | `/move?title=X&from_project=A&to_project=B` | Reorganize |
| Copy | POST | `/copy?title=X&project=Y&new_name=Z` | Duplicate |
| Download | GET | `/download?title=X&project=Y` | Export content |

---

## Workflow Examples

### Example 1: Organize Your Drive
```bash
# Create archive folder
curl -X POST "http://localhost:8000/create-folder?folder_name=Archive&parent_path=default"

# Move old files there
curl -X POST "http://localhost:8000/move?title=oldfile&from_project=default&to_project=Archive"
```

### Example 2: Backup Important Files
```bash
# Copy to backup
curl -X POST "http://localhost:8000/copy?title=important&project=default&new_name=important_backup"

# Move original to safe folder
curl -X POST "http://localhost:8000/move?title=important&from_project=default&to_project=Backups"
```

### Example 3: Export Before Deletion
```bash
# Download to local
curl "http://localhost:8000/download?title=todelete&project=default" > backup.txt

# Delete after confirming backup
curl -X DELETE "http://localhost:8000/delete?title=todelete&project=default"
```

---

## Phase 2 Coming Soon

Planned for next release:
- Delete entire folders
- View/restore from trash
- Share files and set permissions
- Get detailed metadata
- Folder statistics

---

## Updated Endpoint Count

| Category | Count |
|----------|-------|
| Browsing | 5 |
| File Operations | 5 (new!) |
| File I/O | 3 |
| AI Features | 2 |
| System | 1 |
| **TOTAL** | **16** |

