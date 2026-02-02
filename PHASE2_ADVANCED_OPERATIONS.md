# Phase 2 Advanced Operations

## ✅ Now Available (v4.2.0)

**6 powerful advanced operations** for complete Drive management and recovery!

---

## 📂 DELETE FOLDER

**Remove entire folder and all contents**

```bash
curl -X DELETE "http://localhost:8000/delete-folder?folder_name=OldFolder&parent_path=default"
```

**Response:**
```json
{
  "status": "success",
  "message": "Folder 'OldFolder' and all contents deleted"
}
```

---

## 🗑️ LIST TRASH

**View all deleted files waiting for permanent deletion**

```bash
curl "http://localhost:8000/trash?max_items=50"
```

**Response:**
```json
{
  "status": "success",
  "items_count": 5,
  "items": [
    {
      "name": "old_document.txt",
      "id": "abc123",
      "type": "file",
      "trashed_time": "2026-02-01T10:30:00Z",
      "size_bytes": 1024
    }
  ]
}
```

---

## ↩️ RESTORE FROM TRASH

**Recover a deleted file**

```bash
# Get file_id from /trash endpoint first
curl -X POST "http://localhost:8000/restore?file_id=abc123&restore_to_project=default"
```

**Response:**
```json
{
  "status": "success",
  "message": "File 'old_document' restored to 'default'",
  "file_name": "old_document",
  "restored_to": "default"
}
```

---

## 🧹 EMPTY TRASH

**Permanently delete ALL trashed files**

```bash
curl -X DELETE "http://localhost:8000/empty-trash"
```

**Response:**
```json
{
  "status": "success",
  "message": "Permanently deleted 12 items from trash",
  "items_deleted": 12
}
```

---

## 📊 FOLDER STATISTICS

**Get detailed stats about a folder**

```bash
curl "http://localhost:8000/folder-stats?path=Books"
```

**Response:**
```json
{
  "status": "success",
  "path": "Books",
  "folder_count": 3,
  "file_count": 12,
  "total_items": 15,
  "total_size_bytes": 5242880,
  "total_size_mb": 5.0,
  "file_types": {
    "text/plain": 8,
    "application/pdf": 4,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": 2
  }
}
```

---

## 📋 FILE METADATA

**Get complete file information**

```bash
curl "http://localhost:8000/metadata?title=myfile&project=default"
```

**Response:**
```json
{
  "status": "success",
  "file_id": "abc123xyz",
  "name": "myfile.txt",
  "mime_type": "text/plain",
  "size_bytes": 2048,
  "size_mb": 0.002,
  "created": "2026-01-15T09:00:00Z",
  "modified": "2026-02-01T14:30:00Z",
  "viewed": "2026-02-01T15:00:00Z",
  "owners": ["your.email@gmail.com"],
  "url": "https://drive.google.com/file/d/abc123xyz/view",
  "starred": false,
  "trashed": false,
  "description": "My important file"
}
```

---

## 👥 SHARE FILE

**Share file with others (role: reader, writer, owner)**

```bash
# Share as read-only
curl -X POST "http://localhost:8000/share?title=myfile&project=default&email=friend@gmail.com&role=reader"

# Share for editing
curl -X POST "http://localhost:8000/share?title=myfile&project=default&email=colleague@gmail.com&role=writer"
```

**Response:**
```json
{
  "status": "success",
  "message": "File 'myfile' shared with friend@gmail.com as reader",
  "file": "myfile",
  "shared_with": "friend@gmail.com",
  "role": "reader"
}
```

---

## Complete Advanced Operations Reference

| Operation | Method | Endpoint | Purpose |
|-----------|--------|----------|---------|
| Delete Folder | DELETE | `/delete-folder?folder_name=X&parent_path=Y` | Remove entire folder |
| List Trash | GET | `/trash?max_items=50` | See deleted items |
| Restore | POST | `/restore?file_id=X&restore_to_project=Y` | Recover file |
| Empty Trash | DELETE | `/empty-trash` | Permanent deletion |
| Folder Stats | GET | `/folder-stats?path=X` | Storage info |
| Metadata | GET | `/metadata?title=X&project=Y` | File details |
| Share | POST | `/share?title=X&project=Y&email=Z&role=R` | Grant access |

---

## Workflow Examples

### Example 1: Safe Deletion with Recovery Option
```bash
# Delete with confidence - can be restored
curl -X DELETE "http://localhost:8000/delete?title=maybe_delete&project=default"

# Check trash to see it
curl "http://localhost:8000/trash"

# Restore if needed
curl -X POST "http://localhost:8000/restore?file_id=abc123&restore_to_project=default"

# Or permanently delete
curl -X DELETE "http://localhost:8000/empty-trash"
```

### Example 2: Monitor Folder Size
```bash
# Check how much space Books folder uses
curl "http://localhost:8000/folder-stats?path=Books"

# If too large, move old files to Archive
curl -X POST "http://localhost:8000/move?title=old_book&from_project=Books&to_project=Archive"

# Delete Archive when ready
curl -X DELETE "http://localhost:8000/delete-folder?folder_name=Archive&parent_path=default"
```

### Example 3: Collaborate on Files
```bash
# Get file details first
curl "http://localhost:8000/metadata?title=project&project=default"

# Share with team for viewing
curl -X POST "http://localhost:8000/share?title=project&project=default&email=team@company.com&role=reader"

# Share with editor for modifications
curl -X POST "http://localhost:8000/share?title=project&project=default&email=editor@company.com&role=writer"
```

### Example 4: Organize and Cleanup
```bash
# Get stats before cleanup
curl "http://localhost:8000/folder-stats?path=default"

# Create organized structure
curl -X POST "http://localhost:8000/create-folder?folder_name=Archive&parent_path=default"
curl -X POST "http://localhost:8000/create-folder?folder_name=Active&parent_path=default"

# Move old files to archive
curl -X POST "http://localhost:8000/move?title=completed_project&from_project=default&to_project=Archive"

# Check stats after
curl "http://localhost:8000/folder-stats?path=default"
```

---

## Phase 2 Complete! 

**All essential file management features implemented:**
- ✅ Full folder management
- ✅ Trash recovery system
- ✅ Storage analytics
- ✅ Detailed metadata
- ✅ File sharing

---

## Total Endpoints Now: 21

| Category | Count |
|----------|-------|
| Browsing | 5 |
| File Operations | 5 |
| Advanced Operations | 6 |
| File I/O | 3 |
| AI Features | 2 |
| System | 1 |
| **TOTAL** | **22** |

