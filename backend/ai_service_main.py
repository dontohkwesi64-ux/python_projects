# ai_service/main.py
from dotenv import load_dotenv
import os

load_dotenv()  # loads the .env file

print(os.getenv("DATABASE_URL"))  # just to confirm

import asyncio
from fastapi import FastAPI
from .db import connect_db, disconnect_db, db

app = FastAPI(title="AI Service")

@app.on_event("startup")
async def startup_event():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_db()

@app.get("/health")
async def health_check():
    return {"status": "ok", "db_connected": db._client._connected}  # confirms Prisma connection

# Example endpoint using the database
@app.get("/users")
async def list_users():
    return await db.user.find_many()
