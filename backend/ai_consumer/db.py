import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ai_consumer"

client: AsyncIOMotorClient | None = None
db = None

async def connect_db():
    global client, db
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    print("✅ Connected to MongoDB")

async def disconnect_db():
    global client
    if client:
        client.close()
        print("🔌 Disconnected from MongoDB")
