# app/main.py

from fastapi import FastAPI
from app.auth import router as auth_router
from app.file_routes import router as file_router
from app.database import create_db
from app import utils


app = FastAPI(title="PrivyDrop - Secure File Sharing System")

# Call DB initializer
@app.on_event("startup")
async def startup():
    await create_db()

# Register routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(file_router, prefix="/files", tags=["Files"])
app.include_router(utils.router)


@app.get("/")
def home():
    return {"message": "Welcome to PrivyDrop Secure File Sharing System"}
