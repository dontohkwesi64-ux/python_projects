# backend/ai_consumer_main.py
from fastapi import FastAPI
from ai_consumer.db import connect_db, disconnect_db

import asyncio

app = FastAPI(title="AI Consumer Service")

@app.on_event("startup")

async def startup_event():

    await connect_db()

@app.on_event("shutdown")

async def shutdown_event():

    await disconnect_db()

@app.get("/")

async def root():
    
    return {"message": "AI Consumer Service is running ✅"}
