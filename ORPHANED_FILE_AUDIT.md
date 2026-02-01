# Orphaned File Audit & Repair Guide

## Overview

The orphaned file audit feature identifies files in your Google Drive that are unreachable through normal folder navigation (tree traversal) but are discoverable through Drive search. This inconsistency can occur due to shared files, permission changes, or synchronization issues.

## What are Orphaned Files?

**Orphaned files** are files that:
- ✅ Exist in your Google Drive (found by search)
- ❌ Are NOT reachable by navigating the folder hierarchy from the root
- Often have parents that no longer exist or have broken permission chains

## Current State

Based on an audit of your Drive:
- **Tree traversal files**: 0 files reachable from "default" folder
- **Total PDF files**: 106 files found by search
- **Orphaned PDFs**: 106 files (100% orphaned)

This suggests your "default" folder is currently empty of files, but many PDFs exist elsewhere in your Drive.

## Using the Audit Endpoint

### Endpoint: `POST /audit-orphaned-files`

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_type` | string | "all" | Filter by type: "all", "pdf", or MIME type (e.g., "image/jpeg") |
| `fix` | boolean | True | If true, moves orphaned files to fixed folder; if false, only reports |
| `fixed_folder_name` | string | "Books_Fixed" | Destination folder name for orphaned files |
| `root_path` | string | "default" | Root folder to scan from |
| `max_depth` | integer | 10 | Maximum folder nesting depth for tree traversal |

#### Example Requests

**1. Audit PDFs without making changes**
```bash
POST /audit-orphaned-files?file_type=pdf&fix=false
```

**2. Audit all files and move orphans to "Books_Repaired"**
```bash
POST /audit-orphaned-files?file_type=all&fix=true&fixed_folder_name=Books_Repaired
```

**3. Audit images only from a specific folder**
```bash
POST /audit-orphaned-files?file_type=image/jpeg&fix=false&root_path=MyFolder
```

#### Response Format

```json
{
  "status": "success",
  "tree_file_count": 0,
  "all_file_count": 106,
  "orphaned_count": 106,
  "orphaned_files_preview": [
    {
      "id": "1aFyF7jSCMmt8MCgczS_tptQVFqMppjlj",
      "name": "inkomsten-en-uitgavenformulier.pdf"
    },
    {
      "id": "1ErZwAyAkNolwQ3ukcHYoPiAeO0rBXeGE",
      "name": "inkomsten-en-uitgavenformulier_copy.pdf"
    }
  ],
  "orphaned_files_preview_count": 2,
  "moved_count": 0,
  "moved_files_preview": []
}
```

## How It Works

### 1. Tree Traversal Phase
- Recursively navigates from root folder (`root_path`) to all subfolders
- Collects IDs of all files it encounters
- Respects `max_depth` parameter to avoid infinite recursion
- Uses folder hierarchy: Parent → Children → Grandchildren

### 2. Search Phase
- Queries entire Drive for files matching `file_type`
- Handles paginated results (up to 1000+ files)
- Returns: ID, name, MIME type, and parents for each file

### 3. Comparison Phase
- Identifies files in search results NOT in tree traversal
- These are your "orphaned" files
- May indicate:
  - Broken folder hierarchies
  - Shared files from others
  - Files with no parent folder
  - Permission-related issues

### 4. Optional Repair Phase (if `fix=true`)
- Creates "Books_Fixed" folder if it doesn't exist
- For each orphaned file:
  - Removes ALL current parent relationships
  - Adds as child to "Books_Fixed"
- Moves up to hundreds of files efficiently with progress tracking

## Understanding Your Results

### Case: "106 Orphaned PDFs"

Your Drive shows:
```
Tree Traversal: 0 files from "default"
Search Results: 106 PDFs total
Orphaned: 106 PDFs (100%)
```

**What this means:**
- Your "default" folder has no files directly in it
- 106 PDFs exist elsewhere in your Drive (found by search)
- These PDFs are likely:
  - In other folder hierarchies not rooted at "default"
  - Shared files with external permissions
  - Files in root-level folders not part of "default"

**Recommended action:**
```bash
POST /audit-orphaned-files?file_type=pdf&fix=true&fixed_folder_name=PDFs_Consolidated
```

This will:
1. ✓ Consolidate all 106 orphaned PDFs into a "PDFs_Consolidated" folder
2. ✓ Make them easily accessible from a single location
3. ✓ Preserve original file names and metadata

## Advanced Usage

### Finding Specific File Types
```bash
# Find all spreadsheets
POST /audit-orphaned-files?file_type=application/vnd.google-apps.spreadsheet&fix=false

# Find all documents
POST /audit-orphaned-files?file_type=application/vnd.google-apps.document&fix=false

# Find JPEG images
POST /audit-orphaned-files?file_type=image/jpeg&fix=false
```

### Deeper Folder Traversal
```bash
# Search up to 20 levels deep (slower but more thorough)
POST /audit-orphaned-files?file_type=all&fix=false&max_depth=20

# Search only 5 levels deep (faster)
POST /audit-orphaned-files?file_type=all&fix=false&max_depth=5
```

### Organizing by Parent Folder
After repair, check the `moved_files_preview` to see which files were moved. You can then organize them further:
```bash
# Move repaired files into category folders
POST /create-folder?folder_name=PDF_Books&parent_path=PDFs_Consolidated
POST /create-folder?folder_name=PDF_Docs&parent_path=PDFs_Consolidated
```

## Troubleshooting

### Issue: "Search failed"
- Check Google Drive API credentials
- Verify `GOOGLE_OAUTH_TOKEN_JSON` environment variable is set
- Refresh token using `get_token.py`

### Issue: No orphaned files found
- Your Drive structure is clean and well-organized ✓
- All files are reachable through folder hierarchy
- Consider different `file_type` or `root_path`

### Issue: Too many orphaned files
- Your Drive may have duplicate or scattered files
- Repair in batches: run with `fix=false` first, then `fix=true`
- Consider organizing files into categories before repair

## Safety Notes

⚠️ **Important:**
- `fix=true` **will move files** - always test with `fix=false` first
- Moved files are removed from original parent folders
- File contents and permissions are preserved
- Operations are logged for audit trail

## Next Steps

1. **Audit your Drive**: `POST /audit-orphaned-files?file_type=all&fix=false`
2. **Review results**: Check orphaned file count and preview
3. **Test repair** (optional): Move small batch first
4. **Execute repair** (optional): `POST /audit-orphaned-files?file_type=pdf&fix=true`
5. **Verify**: Check the new "Books_Fixed" folder

## Related Endpoints

- `GET /list` - Browse folders normally
- `GET /tree` - View hierarchical structure
- `GET /search` - Search for specific files
- `POST /create-folder` - Create new organization folders
- `POST /move` - Move individual files
- `POST /copy` - Copy files to multiple locations

---

**Last Updated**: February 1, 2026  
**Version**: 4.2.0  
**API**: Isabella - Google Drive Manager
