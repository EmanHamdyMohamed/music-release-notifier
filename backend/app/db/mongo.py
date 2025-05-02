# from motor.motor_asyncio import AsyncIOMotorClient
import motor
from app.core.config import settings
from motor import motor_asyncio
from app.core.config import settings

print(settings)

# client = motor.motor_asyncio.AsyncIOMotorClient.AsyncIOMotorClient(settings.mongo_uri)

# db = client.get_database(settings.database_name)


client = motor_asyncio.AsyncIOMotorClient(
    settings.mongo_uri,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    retryWrites=True,
    w="majority",
    replicaSet=None
)

db = client.get_database(settings.database_name)