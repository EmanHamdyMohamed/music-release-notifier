import logging
from app.core.config import settings
from motor import motor_asyncio

logger = logging.getLogger(__name__)

# Initialize client and db as None
client = None
db = None


def get_client():
    """Get MongoDB client, creating it if it doesn't exist"""
    global client
    if client is None:
        try:
            logger.info(f"Creating MongoDB client for database: {settings.database_name}")
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
            logger.info("MongoDB client created successfully")
        except Exception as e:
            logger.error(f"Failed to create MongoDB client: {e}")
            raise
    return client


def get_database():
    """Get database instance"""
    global db
    if db is None:
        client = get_client()
        db = client.get_database(settings.database_name)
        logger.info(f"Database instance created: {settings.database_name}")
    return db


# For backward compatibility, create instances
try:
    client = get_client()
    db = get_database()
except Exception as e:
    logger.error(f"Failed to initialize database connection: {e}")
    # Don't raise here to allow the app to start


# FastAPI dependency for database
async def get_db():
    """FastAPI dependency to get database instance"""
    return get_database()
