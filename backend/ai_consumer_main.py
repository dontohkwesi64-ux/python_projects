# backend/ai_consumer_main.py
import asyncio
from fastapi import FastAPI
from ai_consumer.db import connect_db, disconnect_db

app = FastAPI(title="AI Consumer Service")

@app.on_event("startup")
async def startup_event():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_db()

@app.get("/health")
async def health_check():
    return {"status": "AI Consumer Service running ✅"}

# Optional: standalone run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ai_consumer_main:app", host="127.0.0.1", port=8000, reload=True)
