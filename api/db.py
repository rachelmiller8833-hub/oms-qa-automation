import os
from motor.motor_asyncio import AsyncIOMotorClient

# Global references to the MongoDB client and database
client = None
db = None

async def connect_db():
    global client, db
    # Read MongoDB connection details from environment variables
    uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    name = os.getenv("MONGO_DB", "orders_db")

    # Initialize async MongoDB client and database
    client = AsyncIOMotorClient(uri)
    db = client[name]

    # Verify database connectivity on startup
    await db.command("ping")

    # Create indexes required for common query patterns
    await db["orders"].create_index("status")
    await db["orders"].create_index("user_id")


async def close_db():
    global client, db
    # Gracefully close the MongoDB connection on application shutdown
    if client is not None:
        client.close()

    client = None
    db = None


def get_db():
    # Dependency helper used by FastAPI to access the database instance
    return db
