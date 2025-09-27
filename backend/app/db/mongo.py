import logging
from app.core.config import settings
from motor import motor_asyncio

logging.info(f"MongoDB URI: {settings.mongo_uri}")
logging.info(f"Database name: {settings.database_name}")

# Create MongoDB client with better error handling
client = motor_asyncio.AsyncIOMotorClient(
    settings.mongo_uri,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    retryWrites=True,
    w="majority",
    replicaSet=None,
    maxPoolSize=10,
    minPoolSize=1,
    maxIdleTimeMS=30000,
    connect=False  # Don't connect immediately
)

db = client.get_database(settings.database_name)
