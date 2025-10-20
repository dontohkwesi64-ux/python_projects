# backend/ai_service_db.py
from prisma import Prisma

db = Prisma()

async def connect_db():
    await db.connect()
    print("AI Service DB connected ✅")

async def disconnect_db():
    await db.disconnect()
    print("AI Service DB disconnected ❌")
