from fastapi import FastAPI
from pydantic import BaseModel
import os, json
from io import BytesIO
import re
import requests

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

# OpenRouter config
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
OPENROUTER_BASE_URL = "https://openrouter.io/api/v1"
# Popular models available on OpenRouter
AVAILABLE_MODELS = {
    "claude-3-5-sonnet": "anthropic/claude-3.5-sonnet",
    "claude-3-opus": "anthropic/claude-3-opus",
    "gpt-4o": "openai/gpt-4o",
    "gpt-4-turbo": "openai/gpt-4-turbo",
    "llama-2": "meta-llama/llama-2-70b-chat",
    "mistral": "mistralai/mistral-7b-instruct"
}

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
    title="Isabella - Google Drive Manager",
    description="AI-powered Google Drive file manager with OpenRouter AI Integration",
    version="4.1.0",
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


class SummarizeRequest(BaseModel):
    title: str
    project: str = "default"
    max_length: int = 300  # Characters in summary
    model: str = "claude-3-5-sonnet"  # AI model to use (optional, falls back to simple summarization)

# ======================================================
# HELPERS
# ======================================================

def get_or_create_folder(folder_name: str, parent_id: str = DRIVE_FOLDER_ID) -> str:
    """Get or create a folder, return its ID"""
    if not drive:
        raise RuntimeError("Google Drive service not initialized - check GOOGLE_OAUTH_TOKEN_JSON env var")
    
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
        raise RuntimeError("Google Drive service not initialized - check GOOGLE_OAUTH_TOKEN_JSON env var")
    
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
        raise RuntimeError("Google Drive service not initialized - check GOOGLE_OAUTH_TOKEN_JSON env var")
    
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
        raise RuntimeError("Google Drive service not initialized - check GOOGLE_OAUTH_TOKEN_JSON env var")
    
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


def simple_summarize(text: str, max_length: int = 300) -> str:
    """
    Simple extractive summarization (no API key needed)
    Extracts key sentences based on word frequency
    """
    try:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if len(sentences) <= 3:
            return text  # Too short, return as-is
        
        # Calculate sentence scores based on word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words_in_sentence = re.findall(r'\b\w+\b', sentence.lower())
            score = sum(word_freq.get(word, 0) for word in words_in_sentence)
            sentence_scores[i] = score
        
        # Get top sentences (maintain order)
        top_sentences = sorted(
            [(i, s) for i, s in sentence_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        # Sort by original order
        top_indices = sorted([idx for idx, _ in top_sentences])
        summary = " ".join([sentences[i] for i in top_indices])
        
        # Trim to max_length
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
        
        return summary.strip()
    except Exception as e:
        print(f"Error summarizing: {str(e)}")
        return text[:max_length] + "..." if len(text) > max_length else text


def openrouter_summarize(text: str, model: str = "claude-3-5-sonnet", max_length: int = 300) -> str:
    """
    Use OpenRouter to summarize text with AI models
    Models available: claude-3-5-sonnet, claude-3-opus, gpt-4o, gpt-4-turbo, llama-2, mistral
    """
    if not OPENROUTER_API_KEY:
        print("OpenRouter API key not configured, falling back to simple summarization")
        return simple_summarize(text, max_length)
    
    try:
        model_id = AVAILABLE_MODELS.get(model, AVAILABLE_MODELS["claude-3-5-sonnet"])
        
        prompt = f"""Summarize the following text in approximately {max_length} characters. 
Be concise and capture the main points.

TEXT:
{text}

SUMMARY:"""
        
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://railway.app",
                "X-Title": "FastAPI GPT Writer"
            },
            json={
                "model": model_id,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result["choices"][0]["message"]["content"].strip()
            return summary[:max_length] + "..." if len(summary) > max_length else summary
        else:
            print(f"OpenRouter error: {response.status_code} - {response.text}")
            return simple_summarize(text, max_length)
    
    except Exception as e:
        print(f"Error with OpenRouter summarization: {str(e)}")
        return simple_summarize(text, max_length)


# ======================================================
# ENDPOINTS
# ======================================================

@app.get("/")
def health_check():
    return {
        "status": "ok" if drive else "error",
        "message": "API is running" if drive else "Google Drive not initialized",
        "google_drive_ready": bool(drive),
        "openrouter_configured": bool(OPENROUTER_API_KEY),
        "env_vars": {
            "GOOGLE_OAUTH_TOKEN_JSON": "✓ SET" if os.environ.get("GOOGLE_OAUTH_TOKEN_JSON") else "✗ NOT SET",
            "OPENROUTER_API_KEY": "✓ SET" if OPENROUTER_API_KEY else "✗ NOT SET"
        }
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
        all_files = [f["name"] for f in files if f["mimeType"] != "application/vnd.google-apps.folder"]

        return {
            "status": "success",
            "path": path,
            "folders": folders,
            "files": all_files,
            "total": len(all_files)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list files: {str(e)}"
        }


@app.get("/list-all")
def list_all_drive_contents():
    """List ALL folders at root level (ISA_BRAIN)"""
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        res = drive.files().list(
            q=f"'{DRIVE_FOLDER_ID}' in parents and trashed=false",
            fields="files(id, name, mimeType, modifiedTime, size)",
            spaces="drive",
            pageSize=100
        ).execute()

        files = res.get("files", [])
        
        # Separate folders and files
        folders = []
        text_files = []
        
        for f in files:
            if f["mimeType"] == "application/vnd.google-apps.folder":
                folders.append({
                    "name": f["name"],
                    "type": "folder",
                    "modified": f.get("modifiedTime", "N/A")
                })
            else:
                folders.append({
                    "name": f["name"],
                    "type": "file",
                    "size_bytes": f.get("size", 0),
                    "modified": f.get("modifiedTime", "N/A")
                })

        return {
            "status": "success",
            "root_folder": "ISA_BRAIN",
            "total_items": len(files),
            "folders_count": len([f for f in files if f["mimeType"] == "application/vnd.google-apps.folder"]),
            "items": folders
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list drive: {str(e)}"
        }


@app.get("/list-recursive")
def list_recursive(path: str = "default", max_depth: int = 5):
    """List all files and folders recursively (tree structure)"""
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    def build_tree(folder_id: str, depth: int = 0) -> dict:
        if depth > max_depth:
            return {"error": "Max depth reached"}
        
        if not drive:
            return {"error": "Google Drive service not initialized"}
        
        try:
            res = drive.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                fields="files(id, name, mimeType, size, modifiedTime)",
                spaces="drive",
                pageSize=50
            ).execute()
            
            items = res.get("files", [])
            result = {
                "folders": [],
                "files": []
            }
            
            for item in items:
                if item["mimeType"] == "application/vnd.google-apps.folder":
                    result["folders"].append({
                        "name": item["name"],
                        "id": item["id"],
                        "modified": item.get("modifiedTime"),
                        "children": build_tree(item["id"], depth + 1)
                    })
                else:
                    result["files"].append({
                        "name": item["name"],
                        "size_bytes": item.get("size", 0),
                        "modified": item.get("modifiedTime")
                    })
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    try:
        project_folder_id = get_or_create_folder(path)
        tree = build_tree(project_folder_id)
        
        return {
            "status": "success",
            "path": path,
            "tree": tree,
            "max_depth": max_depth
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list recursively: {str(e)}"
        }


@app.get("/search")
def search_drive(query: str, search_in: str = "all"):
    """Search for files across entire drive"""
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        # Build query
        if search_in == "all":
            q = f"name contains '{query}' and trashed=false"
        elif search_in == "folders":
            q = f"name contains '{query}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        elif search_in == "files":
            q = f"name contains '{query}' and mimeType!='application/vnd.google-apps.folder' and trashed=false"
        else:
            q = f"name contains '{query}' and trashed=false"
        
        res = drive.files().list(
            q=q,
            fields="files(id, name, mimeType, parents, modifiedTime, size)",
            spaces="drive",
            pageSize=100
        ).execute()

        results = []
        for item in res.get("files", []):
            results.append({
                "name": item["name"],
                "type": "folder" if item["mimeType"] == "application/vnd.google-apps.folder" else "file",
                "size_bytes": item.get("size", 0),
                "modified": item.get("modifiedTime"),
                "id": item["id"]
            })
        
        return {
            "status": "success",
            "query": query,
            "search_in": search_in,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Search failed: {str(e)}"
        }


@app.get("/list-detailed")
def list_detailed(path: str = "default"):
    """List files with detailed information (size, dates, etc)"""
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        project_folder_id = get_or_create_folder(path)
        
        res = drive.files().list(
            q=f"'{project_folder_id}' in parents and trashed=false",
            fields="files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink)",
            spaces="drive",
            pageSize=100
        ).execute()

        files = res.get("files", [])
        
        detailed_items = []
        for f in files:
            detailed_items.append({
                "name": f["name"],
                "type": "folder" if f["mimeType"] == "application/vnd.google-apps.folder" else "file",
                "size_bytes": int(f.get("size", 0)),
                "size_kb": round(int(f.get("size", 0)) / 1024, 2),
                "created": f.get("createdTime"),
                "modified": f.get("modifiedTime"),
                "url": f.get("webViewLink"),
                "id": f["id"]
            })
        
        return {
            "status": "success",
            "path": path,
            "total_items": len(detailed_items),
            "items": detailed_items
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list detailed: {str(e)}"
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


@app.post("/summarize")
def summarize_file(req: SummarizeRequest):
    """Read and summarize an existing file using OpenRouter AI or simple extraction"""
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
                "message": f"File '{req.title}' not found in project '{req.project}'"
            }
        
        content = read_file_from_drive(file["id"])
        
        # Use OpenRouter if available, otherwise fall back to simple summarization
        if req.model and OPENROUTER_API_KEY:
            summary = openrouter_summarize(content, req.model, req.max_length)
            method = "OpenRouter AI"
        else:
            summary = simple_summarize(content, req.max_length)
            method = "Extractive"
        
        return {
            "status": "success",
            "title": req.title,
            "content_length": len(content),
            "summary": summary,
            "method": method,
            "model": req.model if OPENROUTER_API_KEY else "N/A",
            "project": req.project
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to summarize file: {str(e)}"
        }


@app.get("/models")
def list_available_models():
    """List all available AI models from OpenRouter"""
    return {
        "status": "success",
        "models_available": list(AVAILABLE_MODELS.keys()),
        "openrouter_configured": bool(OPENROUTER_API_KEY),
        "model_details": {
            "claude-3-5-sonnet": "Latest Claude 3.5 Sonnet - Best for summarization",
            "claude-3-opus": "Claude 3 Opus - More powerful reasoning",
            "gpt-4o": "OpenAI GPT-4o - Multimodal capabilities",
            "gpt-4-turbo": "GPT-4 Turbo - Fast processing",
            "llama-2": "Meta Llama 2 - Open-source, cost-effective",
            "mistral": "Mistral 7B - Fast and efficient"
        }
    }


@app.get("/diagnose")
def diagnose_system():
    """Diagnose API and Google Drive connection status"""
    diagnostics = {
        "api_status": "✓ OK" if drive else "✗ ERROR",
        "google_drive_initialized": bool(drive),
        "environment_variables": {
            "GOOGLE_OAUTH_TOKEN_JSON_set": bool(os.environ.get("GOOGLE_OAUTH_TOKEN_JSON")),
            "OPENROUTER_API_KEY_set": bool(OPENROUTER_API_KEY)
        },
        "drive_folder_id": DRIVE_FOLDER_ID,
        "recommendations": []
    }
    
    # Check what's wrong
    if not drive:
        diagnostics["recommendations"].append(
            "⚠️  Google Drive NOT initialized. Set GOOGLE_OAUTH_TOKEN_JSON on Railway."
        )
    else:
        diagnostics["recommendations"].append("✓ Google Drive is properly connected")
        
    if not OPENROUTER_API_KEY:
        diagnostics["recommendations"].append(
            "⚠️  OpenRouter not configured. Set OPENROUTER_API_KEY for AI features."
        )
    else:
        diagnostics["recommendations"].append("✓ OpenRouter API is configured")
    
    # Try to actually list the ISA_BRAIN folder
    if drive:
        try:
            about = drive.about().get(fields='storageQuota').execute()
            diagnostics["storage_quota"] = {
                "limit_gb": about.get('storageQuota', {}).get('limit', 0) / (1024**3),
                "usage_gb": about.get('storageQuota', {}).get('usage', 0) / (1024**3)
            }
            
            # List files in ISA_BRAIN
            res = drive.files().list(
                q=f"'{DRIVE_FOLDER_ID}' in parents and trashed=false",
                fields="files(name, mimeType, id, createdTime)",
                pageSize=10
            ).execute()
            
            files = res.get("files", [])
            diagnostics["drive_folder_contents"] = {
                "folder_id": DRIVE_FOLDER_ID,
                "files_count": len(files),
                "files": [{"name": f["name"], "type": f["mimeType"]} for f in files[:5]]
            }
        except Exception as e:
            diagnostics["drive_error"] = str(e)
            diagnostics["recommendations"].append(f"Google Drive error: {str(e)}")
    
    return diagnostics


# ======================================================
# FILE MANAGEMENT OPERATIONS (Phase 1)
# ======================================================

@app.delete("/delete")
def delete_file(title: str, project: str = "default"):
    """Delete a file permanently"""
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
        
        drive.files().delete(fileId=file["id"]).execute()
        
        return {
            "status": "success",
            "message": f"File '{title}' deleted from project '{project}'"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to delete file: {str(e)}"
        }


@app.post("/create-folder")
def create_folder_endpoint(folder_name: str, parent_path: str = "default"):
    """Create a new folder inside an existing folder"""
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        parent_id = get_or_create_folder(parent_path)
        
        # Create the new folder
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }
        
        folder = drive.files().create(
            body=file_metadata,
            fields="id, name"
        ).execute()
        
        return {
            "status": "success",
            "message": f"Folder '{folder_name}' created",
            "folder_id": folder.get("id"),
            "folder_name": folder.get("name")
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create folder: {str(e)}"
        }


@app.post("/move")
def move_file(title: str, from_project: str, to_project: str):
    """Move file from one folder to another"""
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        # Find file in source project
        file = find_file(title, from_project)
        
        if not file:
            return {
                "status": "error",
                "message": f"File '{title}' not found in project '{from_project}'"
            }
        
        # Get destination folder ID
        dest_folder_id = get_or_create_folder(to_project)
        
        # Get source folder ID to remove from
        source_folder_id = get_or_create_folder(from_project)
        
        # Move the file
        drive.files().update(
            fileId=file["id"],
            addParents=dest_folder_id,
            removeParents=source_folder_id,
            fields="id, parents"
        ).execute()
        
        return {
            "status": "success",
            "message": f"File '{title}' moved from '{from_project}' to '{to_project}'"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to move file: {str(e)}"
        }


@app.post("/copy")
def copy_file(title: str, project: str = "default", new_name: str = ""):
    """Copy a file within the same project or to another project"""
    if not drive:
        return {
            "status": "error",
            "message": "Google Drive service not initialized"
        }
    
    try:
        # Find the file to copy
        file = find_file(title, project)
        
        if not file:
            return {
                "status": "error",
                "message": f"File '{title}' not found in project '{project}'"
            }
        
        # Get project folder ID
        project_folder_id = get_or_create_folder(project)
        
        # Create copy metadata
        copy_name = new_name if new_name else f"{title}_copy"
        copy_metadata = {
            "name": f"{copy_name}.txt",
            "parents": [project_folder_id]
        }
        
        # Copy the file
        copy_file_obj = drive.files().copy(
            fileId=file["id"],
            body=copy_metadata,
            fields="id, name"
        ).execute()
        
        return {
            "status": "success",
            "message": f"File copied as '{copy_name}'",
            "original": title,
            "copy_name": copy_name,
            "copy_id": copy_file_obj.get("id")
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to copy file: {str(e)}"
        }


@app.get("/download")
def download_file(title: str, project: str = "default"):
    """Download/export file content as raw text"""
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
                "message": f"File '{title}' not found in project '{project}'"
            }
        
        content = read_file_from_drive(file["id"])
        
        return {
            "status": "success",
            "filename": f"{title}.txt",
            "project": project,
            "content": content,
            "content_length": len(content)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to download file: {str(e)}"
        }


# Book and Series endpoints removed - focusing on Google Drive management only
