"""
MongoEngine database configuration and initialization
"""
import logging
from mongoengine import connect, disconnect
from app.core.config import settings

logger = logging.getLogger(__name__)

# Global connection state
_connected = False


def init_database():
    """Initialize MongoEngine database connection"""
    global _connected
    
    try:
        if _connected:
            logger.info("Database already connected")
            return True
            
        # Connect to MongoDB using MongoEngine
        allow_invalid_host_cert = "true"
        read_preference = 'primaryPreferred'
        print('jjjjjjjjjjjjjjjjjj')
        connect(
            host=f"{settings.mongo_uri}/{settings.database_name}"
                "?retryWrites=true&w=majority&serverSelectionTimeoutMS=10000"
                f"&tlsAllowInvalidHostnames={allow_invalid_host_cert}&tlsAllowInvalidCertificates={allow_invalid_host_cert}&tls=true&readPreference={read_preference}"
        )
        
        _connected = True
        logger.info(f"MongoEngine database connected: {settings.database_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoEngine database: {e}")
        return False


def test_connection() -> bool:
    """Test database connection"""
    try:
        if not _connected:
            return False
            
        # Test connection by importing models (this will trigger connection)
        from app.models.mongoengine_models import User
        # Try a simple operation
        User.objects.count()
        logger.info("Database connection test successful")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False


def close_connection():
    """Close database connection"""
    global _connected
    
    if _connected:
        disconnect()
        _connected = False
        logger.info("Database connection closed")


def get_database():
    """Get database instance (MongoEngine doesn't expose this directly)"""
    return None  # MongoEngine manages connections internally
