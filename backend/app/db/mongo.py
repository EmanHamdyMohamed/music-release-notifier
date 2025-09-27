import logging
from app.core.config import settings
from motor import motor_asyncio

# Log configuration
logging.info(f"MongoDB URI: {settings.mongo_uri}")
logging.info(f"Database name: {settings.database_name}")

# Create MongoDB client optimized for serverless
client = motor_asyncio.AsyncIOMotorClient(
    settings.mongo_uri,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    retryWrites=True,
    w="majority",
    replicaSet=None,
    maxPoolSize=1,  # Reduced for serverless
    minPoolSize=0,  # Reduced for serverless
    maxIdleTimeMS=30000,
    connect=False  # Don't connect immediately
)

db = client.get_database(settings.database_name)
