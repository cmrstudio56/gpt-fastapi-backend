from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="GPT Writer API",
    description="Backend for Custom GPT Actions",
    version="1.0.0"
)

class WriteRequest(BaseModel):
    title: str
    content: str

class WriteResponse(BaseModel):
    status: str
    message: str

@app.post("/write", response_model=WriteResponse)
def write_text(req: WriteRequest):
    filename = f"{req.title}.txt"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(req.content + "\n\n")

    return {
        "status": "success",
        "message": f"Content saved to {filename}"
    }
