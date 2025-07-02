# app/database.py

from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./privydrop.db"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

async def create_db():
    await database.connect()
    # Tables create karenge models se (ye step baad me link hoga)
    metadata.create_all(engine)
