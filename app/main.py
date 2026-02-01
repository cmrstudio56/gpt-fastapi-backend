from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="GPT Writer API",
    description="Backend for Custom GPT Actions",
    version="1.0.0",
    servers=[
        {
            "url": "https://web-production-99e37.up.railway.app",
            "description": "Production server"
        }
    ]
)

class WriteRequest(BaseModel):
    title: str
    content: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}

@app.post("/write")
def write_text(req: WriteRequest):
    filename = f"{req.title}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(req.content + "\n\n")
    return {"status": "success", "message": f"Content saved to {filename}"}

@app.get("/read")
def read_text(title: str):
    filename = f"{title}.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return {
                "status": "success",
                "content": f.read()
            }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"{filename} not found"
        }
