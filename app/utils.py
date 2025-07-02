from fastapi import APIRouter
from cryptography.fernet import Fernet

router = APIRouter()

fernet = Fernet(b"I9h68KNt_yJsSpM9hM655Rzr5u3qWauP1yHJa3MXX5s=")

@router.get("/encrypt-id/{file_id}")
def encrypt_id(file_id: int):
    token = fernet.encrypt(str(file_id).encode()).decode()
    return {"encrypted_id": token}
