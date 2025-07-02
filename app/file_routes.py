from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from sqlalchemy import insert, select
from app.database import database
from app.models import files, users
from jose import jwt, JWTError
from cryptography.fernet import Fernet
import shutil
import os

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
fernet = Fernet(b"I9h68KNt_yJsSpM9hM655Rzr5u3qWauP1yHJa3MXX5s=")

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper to decode JWT
async def get_current_user(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Upload Endpoint
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...), current_user=Depends(get_current_user)
):
    if current_user["role"] != "ops":
        raise HTTPException(status_code=403, detail="Only ops users can upload files")
    
    ext = file.filename.split(".")[-1]
    if ext not in ["pptx", "docx", "xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    query = insert(files).values(
        filename=file.filename,
        uploaded_by=None  # we can link user id if you want
    )
    await database.execute(query)
    
    return {"message": "File uploaded successfully"}

# List Files Endpoint
@router.get("/list")
async def list_files(current_user=Depends(get_current_user)):
    query = select(files)
    rows = await database.fetch_all(query)
    return [{"filename": r["filename"], "id": r["id"]} for r in rows]

# Download Endpoint
@router.get("/download/{encrypted_id}")
async def download_file(encrypted_id: str, current_user=Depends(get_current_user)):
    if current_user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can download")
    
    try:
        file_id = int(fernet.decrypt(encrypted_id.encode()).decode())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid encrypted ID")
    
    query = select(files).where(files.c.id == file_id)
    file = await database.fetch_one(query)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = os.path.join(UPLOAD_DIR, file["filename"])
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return {
        "download-link": f"/files/download-direct/{encrypted_id}",
        "message": "success"
    }

# Direct Download Endpoint (returns file)
from fastapi.responses import FileResponse

@router.get("/download-direct/{encrypted_id}")
async def download_direct(encrypted_id: str, current_user=Depends(get_current_user)):
    if current_user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can download")
    
    try:
        file_id = int(fernet.decrypt(encrypted_id.encode()).decode())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid encrypted ID")
    
    query = select(files).where(files.c.id == file_id)
    file = await database.fetch_one(query)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = os.path.join(UPLOAD_DIR, file["filename"])
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(file_path, filename=file["filename"])
