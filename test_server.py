#!/usr/bin/env python3
"""Test FastAPI server with audit endpoint"""
import sys
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

DRIVE_FOLDER_ID = "1UNIpr8fEWbGccnyAAu01kwXa6xwPdkFk"
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Load credentials
with open('token.json', 'r') as f:
    creds_data = json.load(f)

creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
drive = build('drive', 'v3', credentials=creds)

app = FastAPI()

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
        
        return folder.get("id")
    except Exception as e:
        print(f"Error with folder {folder_name}: {str(e)}")
        raise

@app.post("/audit-orphaned-files")
def audit_orphaned():
    """Test audit endpoint"""
    try:
        print("Starting audit...")
        
        # Get folder
        root_folder_id = get_or_create_folder("default")
        print(f"Root folder: {root_folder_id}")
        
        # Collect tree files
        print("Collecting tree file IDs...")
        tree_file_ids = set()
        res = drive.files().list(
            q=f"'{root_folder_id}' in parents and trashed=false",
            fields="files(id, mimeType)",
            spaces="drive",
            pageSize=100
        ).execute()
        tree_file_ids.update(f["id"] for f in res.get("files", []) if f["mimeType"] != "application/vnd.google-apps.folder")
        print(f"Tree files: {len(tree_file_ids)}")
        
        # Search for PDFs
        print("Searching for PDFs...")
        all_files = []
        res = drive.files().list(
            q="mimeType='application/pdf' and trashed=false",
            fields="files(id, name, mimeType, parents)",
            spaces="drive",
            pageSize=1000
        ).execute()
        all_files.extend(res.get("files", []))
        print(f"PDFs found: {len(all_files)}")
        
        # Find orphans
        orphaned = [f for f in all_files if f["id"] not in tree_file_ids]
        print(f"Orphaned PDFs: {len(orphaned)}")
        
        # Return summary
        return {
            "status": "success",
            "tree_file_count": len(tree_file_ids),
            "all_file_count": len(all_files),
            "orphaned_count": len(orphaned),
            "orphaned_files_preview": [{"id": f["id"], "name": f["name"]} for f in orphaned[:5]],
            "orphaned_files_preview_count": min(5, len(orphaned))
        }
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    print("Starting test server...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
