"""
Beanie database configuration and initialization
"""
import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.models.beanie_models import User, Notification

logger = logging.getLogger(__name__)

# Global variables for client and database
_client: AsyncIOMotorClient = None
_database = None


async def init_database():
    """Initialize Beanie database connection"""
    global _client, _database
    
    try:
        # Create MongoDB client
        _client = AsyncIOMotorClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=5000,
            retryWrites=True,
            w="majority",
            replicaSet=None,
            maxPoolSize=1,  # Reduced for serverless
            minPoolSize=0,  # Reduced for serverless
            maxIdleTimeMS=10000,  # Reduced for serverless
            connect=False,  # Don't connect immediately
            directConnection=False  # Allow connection pooling
        )
        
        # Get database
        _database = _client.get_database(settings.database_name)
        
        # Initialize Beanie with document models
        await init_beanie(
            database=_database,
            document_models=[User, Notification]
        )
        
        logger.info(f"Beanie database initialized: {settings.database_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Beanie database: {e}")
        return False


async def test_connection() -> bool:
    """Test database connection"""
    try:
        if _client is None:
            return False
            
        # Test connection with ping
        await _client.admin.command('ping')
        logger.info("Database connection test successful")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False


async def close_connection():
    """Close database connection"""
    global _client, _database
    
    if _client:
        _client.close()
        _client = None
        _database = None
        logger.info("Database connection closed")


def get_database():
    """Get database instance"""
    return _database


def get_client():
    """Get MongoDB client"""
    return _client
