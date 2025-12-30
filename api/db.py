import os
from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None

async def connect_db():
    global client, db
    uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    name = os.getenv("MONGO_DB", "orders_db")
    client = AsyncIOMotorClient(uri)
    db = client[name]
    await db.command("ping")
    await db["orders"].create_index("status")
    await db["orders"].create_index("user_id")


async def close_db():
    global client,db
    if client is not None:
        client.close()

    client = None
    db = None

def get_db():
    return db