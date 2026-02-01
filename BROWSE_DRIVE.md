# 📂 Complete Google Drive Browsing Guide

Your API now has **5 powerful listing endpoints** to see and organize ALL your Google Drive content!

---

## 🚀 All Listing Endpoints

### 1. **`/list-all`** - See ALL Root Folders
**Shows everything at the top level of your ISA_BRAIN folder**

```bash
curl https://web-production-99e37.up.railway.app/list-all
```

**Response Example:**
```json
{
  "status": "success",
  "root_folder": "ISA_BRAIN",
  "total_items": 15,
  "folders_count": 12,
  "items": [
    {
      "name": "Books",
      "type": "folder",
      "modified": "2025-12-15T10:30:00Z"
    },
    {
      "name": "Projects",
      "type": "folder",
      "modified": "2026-01-20T14:45:00Z"
    },
    {
      "name": "README.txt",
      "type": "file",
      "size_bytes": 1024,
      "modified": "2026-01-15T09:00:00Z"
    }
  ]
}
```

---

### 2. **`/list`** - List Single Folder
**Shows files and subfolders in a specific project**

```bash
# List "default" project
curl "https://web-production-99e37.up.railway.app/list?path=default"

# List "Books" folder
curl "https://web-production-99e37.up.railway.app/list?path=Books"

# List nested folder
curl "https://web-production-99e37.up.railway.app/list?path=Books/Fantasy"
```

**Response:**
```json
{
  "status": "success",
  "path": "Books",
  "folders": ["Fantasy", "SciFi", "NonFiction"],
  "files": ["reading_list.txt", "wishlist.txt"],
  "total": 2
}
```

---

### 3. **`/list-detailed`** - Full File Details
**Shows size, dates, links, and more for each file**

```bash
curl "https://web-production-99e37.up.railway.app/list-detailed?path=Books"
```

**Response:**
```json
{
  "status": "success",
  "path": "Books",
  "total_items": 5,
  "items": [
    {
      "name": "Fantasy",
      "type": "folder",
      "created": "2025-11-01T08:00:00Z",
      "modified": "2026-01-20T15:30:00Z",
      "id": "folder_id_123"
    },
    {
      "name": "reading_list.txt",
      "type": "file",
      "size_bytes": 2048,
      "size_kb": 2.0,
      "created": "2025-12-01T10:00:00Z",
      "modified": "2026-01-25T11:20:00Z",
      "url": "https://drive.google.com/file/d/...",
      "id": "file_id_456"
    }
  ]
}
```

---

### 4. **`/list-recursive`** - Tree View (All Nested Content)
**Shows EVERYTHING - all folders and files in a nested tree structure**

```bash
# Show entire tree from root
curl "https://web-production-99e37.up.railway.app/list-recursive?path=default&max_depth=5"

# Show tree from Books folder
curl "https://web-production-99e37.up.railway.app/list-recursive?path=Books&max_depth=10"
```

**Response:**
```json
{
  "status": "success",
  "path": "Books",
  "max_depth": 5,
  "tree": {
    "folders": [
      {
        "name": "Fantasy",
        "id": "folder_123",
        "modified": "2026-01-20T15:30:00Z",
        "children": {
          "folders": [
            {
              "name": "Series",
              "id": "folder_124",
              "children": {
                "folders": [],
                "files": [
                  {
                    "name": "The-First-Book.txt",
                    "size_bytes": 50000,
                    "modified": "2026-01-15T09:00:00Z"
                  }
                ]
              }
            }
          ],
          "files": [
            {
              "name": "wishlist.txt",
              "size_bytes": 1024,
              "modified": "2026-01-10T14:00:00Z"
            }
          ]
        }
      }
    ],
    "files": []
  }
}
```

---

### 5. **`/search`** - Find Files Anywhere
**Search across your entire drive**

```bash
# Search for files containing "novel"
curl "https://web-production-99e37.up.railway.app/search?query=novel&search_in=all"

# Search only in folder names
curl "https://web-production-99e37.up.railway.app/search?query=chapter&search_in=folders"

# Search only in file names
curl "https://web-production-99e37.up.railway.app/search?query=draft&search_in=files"
```

**Response:**
```json
{
  "status": "success",
  "query": "novel",
  "search_in": "all",
  "results_count": 3,
  "results": [
    {
      "name": "novel_outline.txt",
      "type": "file",
      "size_bytes": 5000,
      "modified": "2026-01-20T10:00:00Z",
      "id": "file_xyz"
    },
    {
      "name": "novel_characters",
      "type": "folder",
      "size_bytes": 0,
      "modified": "2026-01-18T14:30:00Z",
      "id": "folder_xyz"
    }
  ]
}
```

---

## 📋 Comparison Table

| Endpoint | Use Case | Details | Max Items |
|----------|----------|---------|-----------|
| `/list-all` | See all root folders | Minimal info | 100 |
| `/list` | View one folder | Names only | 100 |
| `/list-detailed` | See sizes & dates | Full metadata | 100 |
| `/list-recursive` | See entire tree | Nested structure | Unlimited (depth limit) |
| `/search` | Find files fast | Global search | 100 |

---

## 💡 Usage Examples for Your GPT

### Example 1: Browse Your Library
```bash
# See all your book projects
curl "https://web-production-99e37.up.railway.app/list-all"
# Then drill into one:
curl "https://web-production-99e37.up.railway.app/list-detailed?path=Books"
```

### Example 2: Find All Drafts
```bash
curl "https://web-production-99e37.up.railway.app/search?query=draft&search_in=files"
```

### Example 3: See Complete Project Structure
```bash
curl "https://web-production-99e37.up.railway.app/list-recursive?path=MyNovel&max_depth=10"
```

### Example 4: Organize by Checking Sizes
```bash
curl "https://web-production-99e37.up.railway.app/list-detailed?path=Projects"
# See which files are largest, organize accordingly
```

---

## 🎯 Via Custom GPT

Your Custom GPT can now use these endpoints to:

1. **"Show me all my folders"** → `/list-all`
2. **"What's in my Books folder?"** → `/list?path=Books`
3. **"Show me everything with file sizes"** → `/list-detailed?path=Books`
4. **"Show me the complete structure"** → `/list-recursive?path=default`
5. **"Find all files with 'draft' in the name"** → `/search?query=draft`

---

## 🔧 Parameters

### Common Parameters:
- **`path`** - Folder name (default: "default")
- **`query`** - Search term
- **`search_in`** - "all", "folders", or "files"
- **`max_depth`** - How deep to recurse (default: 5, max: 10)

---

## ✨ Now You Can:

✅ See everything at a glance (`/list-all`)  
✅ Browse into specific folders (`/list`)  
✅ See file sizes and dates (`/list-detailed`)  
✅ View complete nested structure (`/list-recursive`)  
✅ Search across entire drive (`/search`)  
✅ Use GPT to organize and manage it all!

---

## 📌 API Version: 3.6.0
All endpoints fully tested and ready for production! 🚀
