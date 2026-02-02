"""
ISABELLA - MASTER STORYTELLER GPT
Advanced FastAPI Backend for Professional Story Generation
Version 5.0 - Elite Writer Architecture
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os
import json
import requests
from io import BytesIO
from datetime import datetime
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Google Drive & Auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# ========================================
# CONFIGURATION
# ========================================

SCOPES = ["https://www.googleapis.com/auth/drive"]
DRIVE_FOLDER_ID = "1UNIpr8fEWbGccnyAAu01kwXa6xwPdkFk"  # ISA_BRAIN root

# OpenRouter Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
if not OPENROUTER_API_KEY:
    try:
        with open("fastapi openrouter .txt", "r") as f:
            OPENROUTER_API_KEY = f.read().strip()
    except:
        pass

OPENROUTER_BASE_URL = "https://openrouter.io/api/v1"

# Primary writing models (in priority order)
WRITING_MODELS = {
    "claude-3-5-sonnet": "anthropic/claude-3.5-sonnet",      # Best for narrative
    "gpt-4o": "openai/gpt-4o",                               # Best for dialogue
    "claude-3-opus": "anthropic/claude-3-opus",              # Alternative narrative
    "claude-3.5-opus": "anthropic/claude-3.5-opus",          # User requested "Opus 4.5" capability
    "llama-2": "meta-llama/llama-2-70b-chat"                 # Experimental/diverse
}

# ========================================
# GOOGLE DRIVE AUTHENTICATION
# ========================================

def get_drive_service():
    """Initialize Google Drive service with OAuth"""
    creds = None
    
    # Railway production
    if os.environ.get("GOOGLE_OAUTH_TOKEN_JSON"):
        try:
            creds = Credentials.from_authorized_user_info(
                json.loads(os.environ["GOOGLE_OAUTH_TOKEN_JSON"]),
                SCOPES
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load credentials from env: {str(e)}")
    
    # Local development
    elif os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception as e:
            raise RuntimeError(f"Failed to load token.json: {str(e)}")
    
    # First-time OAuth
    else:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as f:
                f.write(creds.to_json())
        except FileNotFoundError:
            raise RuntimeError("client_secret.json not found")
        except Exception as e:
            raise RuntimeError(f"OAuth flow failed: {str(e)}")
    
    return build("drive", "v3", credentials=creds)

try:
    drive = get_drive_service()
except Exception as e:
    print(f"ERROR: Google Drive not initialized: {str(e)}")
    drive = None

# ========================================
# FASTAPI APP
# ========================================

app = FastAPI(
    title="Isabella - Master Storyteller",
    description="Elite professional story generation with Google Drive integration",
    version="5.0.0",
    servers=[{
        "url": "https://web-production-99e37.up.railway.app",
        "description": "Production server"
    }]
)

# ========================================
# DATA MODELS
# ========================================

class StoryPrompt(BaseModel):
    prompt: str
    genre: str = "auto"  # auto-detect or specify (literary, scifi, thriller, etc.)
    length: str = "chapter"  # chapter (3-4k), short (1-2k), long (5-8k)
    project_name: str = "Isabella_Stories"
    model: str = "claude-3-5-sonnet"

class StoryTitle(BaseModel):
    project_name: str
    title: str = "Untitled"

class ContinueStory(BaseModel):
    project_name: str
    context: str  # Brief recap of where story left off
    model: str = "claude-3-5-sonnet"

class ReviseChapter(BaseModel):
    project_name: str
    chapter_num: int
    feedback: str  # What needs to change (tone, pacing, etc.)
    model: str = "claude-3-5-sonnet"

# ========================================
# OPENROUTER INTEGRATION
# ========================================

def call_writer_model(prompt: str, model: str = "claude-3-5-sonnet", system_instruction: str = None) -> str:
    """
    Call OpenRouter API with Isabella system instruction
    Returns generated story text
    """
    
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not configured")
    
    model_key = WRITING_MODELS.get(model, WRITING_MODELS["claude-3-5-sonnet"])
    
    # Isabella master system instruction
    system = system_instruction or """You are Isabella, a master storyteller and professional author with 20+ years of published experience across fiction, screenwriting, and long-form narrative.

CRITICAL DIRECTIVES:
1. Write publishable-quality prose immediately (not drafts)
2. Show, never tell. Subtext drives narrative.
3. Every scene is necessary. No filler, no redundancy.
4. Character authenticity: genuine motivation, never plot convenience.
5. Dialogue reveals character or advances plot—never explanatory.
6. Thematic depth: stories resonate beyond their surface plot.
7. Unique voice for each story—never template-driven.
8. Assume intelligent reader. Trust them to discover meaning.

YOUR RESPONSIBILITY:
- Generate complete, publishable scenes (minimum 500 words per scene)
- Maintain tonal and stylistic consistency within story
- Escalate stakes and emotional resonance continuously
- Make creative decisions unilaterally without apology
- Deliver work that would be accepted by major literary agents

WRITE NOW. No explanations. No outlines. Only complete scenes."""
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://isabella.ai",
        "X-Title": "Isabella Story Generator"
    }
    
    payload = {
        "model": model_key,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 8000,
        "top_p": 0.95,
    }
    
    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            raise RuntimeError("Invalid OpenRouter response")
    
    except Exception as e:
        raise RuntimeError(f"OpenRouter API error: {str(e)}")

def get_or_create_folder(folder_name: str, parent_id: str = DRIVE_FOLDER_ID) -> str:
    """Get or create a folder in Google Drive"""
    if not drive:
        raise RuntimeError("Google Drive not initialized")
    
    try:
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
        res = drive.files().list(q=query, fields="files(id, name)", spaces="drive").execute()
        
        if res.get("files"):
            return res["files"][0]["id"]
        
        # Create if doesn't exist
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }
        folder = drive.files().create(body=metadata, fields="id").execute()
        return folder.get("id")
    
    except Exception as e:
        raise RuntimeError(f"Folder operation failed: {str(e)}")

def save_chapter_to_drive(project_name: str, chapter_title: str, content: str, chapter_num: int = None) -> dict:
    """Save story chapter to Google Drive"""
    if not drive:
        raise RuntimeError("Google Drive not initialized")
    
    try:
        # Get or create project folder
        project_folder_id = get_or_create_folder(project_name)
        
        # Create filename
        if chapter_num:
            filename = f"Chapter_{chapter_num}_{chapter_title}.txt"
        else:
            filename = f"{chapter_title}.txt"
        
        # Create file in Drive
        file_metadata = {
            "name": filename,
            "parents": [project_folder_id]
        }
        
        file = drive.files().create(
            body=file_metadata,
            media_body=MediaIoBaseUpload(
                BytesIO(content.encode('utf-8')),
                mimetype='text/plain'
            ),
            fields='id, webViewLink'
        ).execute()
        
        return {
            "file_id": file.get("id"),
            "filename": filename,
            "folder": project_name,
            "link": file.get("webViewLink"),
            "created_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise RuntimeError(f"Save failed: {str(e)}")

# ========================================
# ISABELLA STORY ENDPOINTS
# ========================================

@app.post("/story/create")
async def create_story(request: StoryPrompt):
    """
    Isabella writes a new story from a single prompt.
    Automatically saves to Google Drive.
    Returns: chapter content + Google Drive link
    """
    if not drive:
        return JSONResponse(status_code=500, content={"error": "Google Drive not initialized"})
    
    try:
        # Build writing prompt
        writing_prompt = f"""
STORY PROMPT: {request.prompt}

REQUIREMENTS:
- Write the opening chapter/scene of this story
- Length: {request.length} (aim for {'3000-4000 words' if request.length == 'chapter' else '1000-2000 words' if request.length == 'short' else '5000-8000 words'})
- Genre: {request.genre if request.genre != 'auto' else 'Determine the best genre for this story'}
- Quality: Publishable, professional prose
- Opening: Strong hook that draws reader in immediately
- End: Scene closure with momentum toward next beat

WRITE THE COMPLETE OPENING CHAPTER NOW:
"""
        
        # Generate story
        story_content = await call_writer_model_async(writing_prompt, request.model)
        
        # Save to Drive
        chapter_title = request.prompt[:50].replace(" ", "_")
        drive_info = save_chapter_to_drive(
            request.project_name,
            chapter_title,
            story_content,
            chapter_num=1
        )
        
        return {
            "status": "success",
            "message": "Story chapter created and saved to Google Drive",
            "chapter": 1,
            "word_count": len(story_content.split()),
            "project": request.project_name,
            "drive_link": drive_info["link"],
            "file_id": drive_info["file_id"],
            "preview": story_content[:500] + "..."
        }
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/story/continue")
async def continue_story(request: ContinueStory):
    """
    Isabella continues an existing story.
    Analyzes previous chapter and escalates naturally.
    Saves next chapter to Google Drive.
    """
    if not drive:
        return JSONResponse(status_code=500, content={"error": "Google Drive not initialized"})
    
    try:
        continuation_prompt = f"""
STORY CONTEXT: {request.context}

WRITE THE NEXT CHAPTER:
- Continue from the emotional and narrative momentum established
- Escalate stakes, complexity, and character revelation
- Maintain established voice and thematic consistency
- Target length: 3000-4000 words
- Open strong, close with cliffhanger or emotional beat
- NO summaries, NO recaps—reader already knows what happened

WRITE CHAPTER NOW:
"""
        
        # Generate continuation
        next_chapter = await call_writer_model_async(continuation_prompt, request.model)
        
        # Save to Drive
        drive_info = save_chapter_to_drive(
            request.project_name,
            "continuation",
            next_chapter,
            chapter_num=None
        )
        
        return {
            "status": "success",
            "message": "Story continued and saved to Google Drive",
            "word_count": len(next_chapter.split()),
            "project": request.project_name,
            "drive_link": drive_info["link"],
            "preview": next_chapter[:500] + "..."
        }
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/story/revise")
async def revise_chapter(request: ReviseChapter):
    """
    Isabella rewrites a chapter based on feedback.
    Fixes structural issues, not just surface changes.
    """
    if not drive:
        return JSONResponse(status_code=500, content={"error": "Google Drive not initialized"})
    
    try:
        revision_prompt = f"""
CHAPTER TO REVISE: Chapter {request.chapter_num}

REVISION NOTES: {request.feedback}

INSTRUCTIONS:
- Identify the root cause of the feedback (not just surface symptoms)
- Rewrite the entire chapter with the correction integrated
- Maintain character consistency and plot continuity
- Keep any elements that work; transform what doesn't
- Preserve the chapter's emotional arc
- Length: original length (3000-4000 words)

WRITE THE REVISED CHAPTER NOW:
"""
        
        # Generate revision
        revised_chapter = await call_writer_model_async(revision_prompt, request.model)
        
        # Save revised version
        drive_info = save_chapter_to_drive(
            request.project_name,
            f"Chapter_{request.chapter_num}_REVISED",
            revised_chapter,
            chapter_num=request.chapter_num
        )
        
        return {
            "status": "success",
            "message": f"Chapter {request.chapter_num} revised and saved",
            "project": request.project_name,
            "drive_link": drive_info["link"],
            "preview": revised_chapter[:500] + "..."
        }
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ========================================
# UTILITY ENDPOINTS
# ========================================

@app.get("/story/models")
async def available_models():
    """List available writing models and their characteristics"""
    return {
        "primary": {
            "claude-3-5-sonnet": "Best for narrative sophistication and character work",
            "gpt-4o": "Best for dialogue precision and world-building",
        },
        "alternative": {
            "claude-3-opus": "Deep thematic exploration, complex plots",
            "llama-2": "Creative range, experimental voices"
        }
    }

@app.get("/story/status")
async def status():
    """Check system status and API connections"""
    return {
        "service": "Isabella Master Storyteller",
        "version": "5.0.0",
        "status": "online",
        "google_drive": "connected" if drive else "disconnected",
        "openrouter": "configured" if OPENROUTER_API_KEY else "missing",
        "timestamp": datetime.now().isoformat()
    }

# ========================================
# HELPER ASYNC WRAPPER
# ========================================

async def call_writer_model_async(prompt: str, model: str) -> str:
    """Async wrapper for writer model call - runs in thread pool to avoid blocking"""
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=1)
    return await loop.run_in_executor(executor, call_writer_model, prompt, model)

# ========================================
# ROOT ENDPOINT
# ========================================

@app.get("/")
async def root():
    """Isabella API - Master Storyteller"""
    return {
        "service": "Isabella - Master Storyteller GPT",
        "version": "5.0.0",
        "status": "online",
        "endpoints": {
            "POST /story/create": "Generate a new story from prompt",
            "POST /story/continue": "Continue an existing story",
            "POST /story/revise": "Revise a specific chapter",
            "GET /story/models": "List available writing models",
            "GET /story/status": "System status"
        },
        "google_drive_integration": "Automatic story saving enabled",
        "openrouter_models": list(WRITING_MODELS.keys())
    }

# ========================================
# RUN
# ========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
