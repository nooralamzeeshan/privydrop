from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import insert, select
from app.database import database
from app.models import users
from jose import jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(Fernet.generate_key())

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    role: str  # "ops" or "client"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(data: SignupRequest):
    query = select(users).where(users.c.email == data.email)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = pwd_context.hash(data.password)
    insert_query = insert(users).values(
        email=data.email,
        hashed_password=hashed_pw,
        role=data.role,
        is_verified=0
    )
    user_id = await database.execute(insert_query)

    encrypted_id = fernet.encrypt(str(user_id).encode()).decode()

    return {
        "message": "Signup successful",
        "download-link": f"/files/download/{encrypted_id}"
    }

@router.post("/login")
async def login(data: LoginRequest):
    query = select(users).where(users.c.email == data.email)
    user = await database.fetch_one(query)
    if not user or not pwd_context.verify(data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = jwt.encode({"sub": user["email"], "role": user["role"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}
