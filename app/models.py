from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, MetaData
from datetime import datetime
from app.database import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=True),  # optional
    Column("email", String, unique=True, index=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("role", String, nullable=False),  # 'ops' or 'client'
    Column("is_verified", Integer, default=0),
)

files = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String, nullable=False),
    Column("uploaded_by", Integer, ForeignKey("users.id")),
    Column("upload_time", DateTime, default=datetime.utcnow),
)
