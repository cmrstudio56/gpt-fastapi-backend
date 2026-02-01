#!/usr/bin/env python3
"""Test orphaned file audit directly"""
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json

DRIVE_FOLDER_ID = "1UNIpr8fEWbGccnyAAu01kwXa6xwPdkFk"
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Load token
with open('token.json', 'r') as f:
    creds_data = json.load(f)

creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
drive = build('drive', 'v3', credentials=creds)

def get_or_create_folder(folder_name: str, parent_id: str = DRIVE_FOLDER_ID) -> str:
    """Get or create a folder, return its ID"""
    try:
        query = (
            f"name='{folder_name}' and "
            f"mimeType='application/vnd.google-apps.folder' and "
            f"'{parent_id}' in parents and trashed=false"
        )
        
        res = drive.files().list(
            q=query,
            fields="files(id, name)",
            spaces="drive"
        ).execute()
        
        files = res.get("files", [])
        if files:
            print(f"  Found existing folder: {folder_name} ({files[0]['id']})")
            return files[0]["id"]
        
        # Create folder if it doesn't exist
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }
        
        folder = drive.files().create(
            body=file_metadata,
            fields="id"
        ).execute()
        
        print(f"  Created new folder: {folder_name} ({folder.get('id')})")
        return folder.get("id")
    except Exception as e:
        print(f"Error with folder {folder_name}: {str(e)}")
        raise

# 1. Collect all reachable file IDs from tree traversal
def collect_tree_file_ids(folder_id: str, depth: int = 0, ids=None, max_depth: int = 10):
    if ids is None:
        ids = set()
    if depth > max_depth:
        return ids
    try:
        res = drive.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id, name, mimeType)",
            spaces="drive",
            pageSize=100
        ).execute()
        for item in res.get("files", []):
            if item["mimeType"] == "application/vnd.google-apps.folder":
                ids = collect_tree_file_ids(item["id"], depth + 1, ids, max_depth)
            else:
                ids.add(item["id"])
    except Exception as e:
        print(f"Error traversing: {e}")
    return ids

print("\n=== Orphaned File Audit ===\n")

try:
    root_folder_id = get_or_create_folder("default")
    print(f"\nCollecting tree file IDs from: {root_folder_id}")
    tree_file_ids = collect_tree_file_ids(root_folder_id)
    print(f"  Tree traversal found: {len(tree_file_ids)} files")

    # 2. Collect all files by search
    print(f"\nSearching for PDF files...")
    q = "mimeType='application/pdf' and trashed=false"
    res = drive.files().list(
        q=q,
        fields="files(id, name, mimeType, parents)",
        spaces="drive",
        pageSize=1000
    ).execute()
    all_files = res.get("files", [])
    print(f"  Search found: {len(all_files)} PDF files")

    # 3. Identify orphans
    orphaned = [f for f in all_files if f["id"] not in tree_file_ids]
    print(f"\nOrphaned PDFs: {len(orphaned)}")
    
    if orphaned:
        print("\nOrphaned PDF details:")
        for f in orphaned[:10]:  # Show first 10
            parents = f.get("parents", [])
            print(f"  - {f['name']} (ID: {f['id']}, Parents: {parents})")
        if len(orphaned) > 10:
            print(f"  ... and {len(orphaned) - 10} more")
    
    print(f"\n✓ Audit complete!")
    print(f"  Total tree files: {len(tree_file_ids)}")
    print(f"  Total PDFs: {len(all_files)}")
    print(f"  Orphaned: {len(orphaned)}")
    
except Exception as e:
    print(f"\n✗ Audit failed: {e}")
    import traceback
    traceback.print_exc()
