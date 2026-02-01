from fastapi import FastAPI
from pydantic import BaseModel
import os, json
from io import BytesIO

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# ======================================================
# CONFIG
# ======================================================

SCOPES = ["https://www.googleapis.com/auth/drive"]

# ISA_BRAIN folder ID
DRIVE_FOLDER_ID = "1UNIpr8fEWbGccnyAAu01kwXa6xwPdkFk"

# ======================================================
# GOOGLE DRIVE AUTH
# ======================================================

def get_drive_service():
    creds = None

    # Railway / production (token from env)
    if os.environ.get("GOOGLE_OAUTH_TOKEN_JSON"):
        try:
            creds = Credentials.from_authorized_user_info(
                json.loads(os.environ["GOOGLE_OAUTH_TOKEN_JSON"]),
                SCOPES
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load credentials from env: {str(e)}")

    # Local dev (existing token.json)
    elif os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file(
                "token.json", SCOPES
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load token.json: {str(e)}")

    # First-time local OAuth
    else:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as f:
                f.write(creds.to_json())
        except FileNotFoundError:
            raise RuntimeError("client_secret.json not found. Please add Google OAuth credentials.")
        except Exception as e:
            raise RuntimeError(f"OAuth flow failed: {str(e)}")

    return build("drive", "v3", credentials=creds)


try:
    drive = get_drive_service()
except Exception as e:
    print(f"ERROR: Could not initialize Google Drive: {str(e)}")
    drive = None

# ======================================================
# FASTAPI APP
# ======================================================

app = FastAPI(
    title="GPT Writer API",
    description="Backend for Custom GPT Actions",
    version="3.2.0",
    servers=[
        {
            "url": "https://web-production-99e37.up.railway.app",
            "description": "Production server"
        }
    ]
)

# ======================================================
# MODELS
# ======================================================

class WriteRequest(BaseModel):
    title: str
    content: str
    project: str = "default"  # Optional project folder

# ======================================================
# HELPERS
# ======================================================

def get_or_create_folder(folder_name: str, parent_id: str = DRIVE_FOLDER_ID) -> str:
    """Get or create a folder, return its ID"""
    if not drive:
        raise RuntimeError("Google Drive service not initialized")
    
    try:
        # Check if folder exists
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


def find_file(title: str, project: str = "default"):
    """Find a file by title in a project folder"""
    if not drive:
        return None
    
    try:
        # Get project folder ID
        project_folder_id = get_or_create_folder(project)
        
        query = (
            f"name='{title}.txt' and "
            f"'{project_folder_id}' in parents and trashed=false"
        )

        res = drive.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()

        files = res.get("files", [])
        return files[0] if files else None
    except Exception as e:
        print(f"Error finding file {title}: {str(e)}")
        return None


def create_file(title: str, content: str, project: str = "default"):
    """Create a new file in a project folder"""
    if not drive:
        raise RuntimeError("Google Drive service not initialized")
    
    try:
        # Get or create project folder
        project_folder_id = get_or_create_folder(project)
        
        metadata = {
            "name": f"{title}.txt",
            "parents": [project_folder_id]
        }

        # Convert string content to file-like object
        content_bytes = content.encode('utf-8')
        media = MediaIoBaseUpload(
            BytesIO(content_bytes),
            mimetype='text/plain',
            resumable=True
        )

        file = drive.files().create(
            body=metadata,
            media_body=media,
            fields="id"
        ).execute()
        
        return file.get("id")
    except Exception as e:
        print(f"Error creating file {title}: {str(e)}")
        raise


def read_file_from_drive(file_id: str):
    """Read content from a file in Google Drive"""
    if not drive:
        raise RuntimeError("Google Drive service not initialized")
    
    try:
        request = drive.files().get_media(fileId=file_id)
        file_content = BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        
        done = False
        while not done:
            _, done = downloader.next_chunk()
        
        return file_content.getvalue().decode("utf-8")
    except Exception as e:
        print(f"Error reading file {file_id}: {str(e)}")
        raise


def append_file(file_id: str, content: str):
    """Append content to an existing file"""
    if not drive:
        raise RuntimeError("Google Drive service not initialized")
    
    try:
        existing = read_file_from_drive(file_id)
        updated = existing + "\n\n" + content

        # Convert string content to file-like object
        content_bytes = updated.encode('utf-8')
        media = MediaIoBaseUpload(
            BytesIO(content_bytes),
            mimetype='text/plain',
            resumable=True
        )

        drive.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
    except Exception as e:
        print(f"Error appending to file {file_id}: {str(e)}")
        raise

# ======================================================
# ENDPOINTS
# ======================================================

@app.get("/")
def health_check():
    return {
        "status": "ok" if drive else "error",
        "message": "API is running" if drive else "Google Drive not initialized"
    }


@app.get("/list")
def list_files(path: str = "default"):
    """List files in a project folder"""
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        # Get the folder ID for the path
        project_folder_id = get_or_create_folder(path)
        
        res = drive.files().list(
            q=f"'{project_folder_id}' in parents and trashed=false",
            fields="files(name, mimeType)",
            spaces="drive"
        ).execute()

        files = res.get("files", [])
        
        # Separate folders and files
        folders = [f["name"] for f in files if f["mimeType"] == "application/vnd.google-apps.folder"]
        text_files = [f["name"] for f in files if f["name"].endswith(".txt")]

        return {
            "status": "success",
            "path": path,
            "folders": folders,
            "files": text_files,
            "total": len(text_files)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list files: {str(e)}"
        }


@app.post("/write")
def write_text(req: WriteRequest):
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        if find_file(req.title, req.project):
            return {
                "status": "error",
                "message": f"File already exists in project '{req.project}'. Use /append."
            }

        file_id = create_file(req.title, req.content, req.project)

        return {
            "status": "success",
            "message": f"File created in project '{req.project}' (ID: {file_id})"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create file: {str(e)}"
        }


@app.get("/read")
def read_text(title: str, project: str = "default"):
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        file = find_file(title, project)
        
        if not file:
            return {
                "status": "error",
                "message": f"File '{title}.txt' not found in project '{project}'"
            }

        content = read_file_from_drive(file["id"])
        
        return {
            "status": "success",
            "content": content,
            "project": project
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read file: {str(e)}"
        }


@app.post("/append")
def append_text(req: WriteRequest):
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        file = find_file(req.title, req.project)

        if not file:
            return {
                "status": "error",
                "message": f"File not found in project '{req.project}'. Use /write first."
            }

        append_file(file["id"], req.content)

        return {
            "status": "success",
            "message": f"Content appended in project '{req.project}'."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to append to file: {str(e)}"
        }
