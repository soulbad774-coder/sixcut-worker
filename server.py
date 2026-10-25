
import os
import secrets
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="SixCut Worker")

WORKER_TOKEN = os.environ.get("WORKER_TOKEN", "")


@app.get("/")
def home():
    return {
        "app": "SixCut Worker",
        "status": "online",
        "processing": "not_configured"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/worker/test")
def test_worker(authorization: str = Header(default="")):
    if not WORKER_TOKEN:
        raise HTTPException(503, "Worker token is not configured")

    expected = f"Bearer {WORKER_TOKEN}"
    if not secrets.compare_digest(authorization, expected):
        raise HTTPException(401, "Unauthorized")

    return {
        "success": True,
        "message": "Secure connection successful"
  }
  
