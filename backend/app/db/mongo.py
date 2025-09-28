import logging
import asyncio
from typing import Optional
from app.core.config import settings
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

# Initialize client and db as None
_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_client() -> AsyncIOMotorClient:
    """Get MongoDB client, creating it if it doesn't exist"""
    global _client
    if _client is None:
        try:
            logger.info(f"Creating MongoDB client for database: {settings.database_name}")
            _client = motor_asyncio.AsyncIOMotorClient(
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
    return _client


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    global _db
    if _db is None:
        client = get_client()
        _db = client.get_database(settings.database_name)
        logger.info(f"Database instance created: {settings.database_name}")
    return _db


async def test_connection() -> bool:
    """Test database connection with timeout"""
    try:
        client = get_client()
        await asyncio.wait_for(
            client.admin.command('ping'),
            timeout=5.0
        )
        return True
    except asyncio.TimeoutError:
        logger.error("Database connection timeout")
        return False
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


async def close_connection():
    """Close database connection"""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("Database connection closed")


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
