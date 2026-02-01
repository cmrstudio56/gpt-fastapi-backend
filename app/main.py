from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(
    title="GPT Writer API",
    description="Backend for Custom GPT Actions",
    version="1.1.0",
    servers=[
        {
            "url": "https://web-production-99e37.up.railway.app",
            "description": "Production server"
        }
    ]
)

# ---------- Models ----------

class WriteRequest(BaseModel):
    title: str
    content: str

class WriteResponse(BaseModel):
    status: str
    message: str

# ---------- Helpers ----------

def filename_from_title(title: str) -> str:
    return f"{title}.txt"

# ---------- Endpoints ----------

@app.post("/write", response_model=WriteResponse)
def write_text(req: WriteRequest):
    filename = filename_from_title(req.title)

    with open(filename, "a", encoding="utf-8") as f:
        f.write(req.content + "\n\n")

    return {
        "status": "success",
        "message": f"Content written to {filename}"
    }


@app.post("/append", response_model=WriteResponse)
def append_text(req: WriteRequest):
    filename = filename_from_title(req.title)

    if not os.path.exists(filename):
        return {
            "status": "error",
            "message": f"{filename} does not exist. Use /write first."
        }

    with open(filename, "a", encoding="utf-8") as f:
        f.write(req.content + "\n\n")

    return {
        "status": "success",
        "message": f"Content appended to {filename}"
    }


@app.get("/read")
def read_text(title: str):
    filename = filename_from_title(title)

    if not os.path.exists(filename):
        return {
            "status": "error",
            "message": f"{filename} not found"
        }

    with open(filename, "r", encoding="utf-8") as f:
        return {
            "status": "success",
            "content": f.read()
        }


@app.get("/list")
def list_files():
    files = [f for f in os.listdir(".") if f.endswith(".txt")]

    return {
        "status": "success",
        "files": files
    }

