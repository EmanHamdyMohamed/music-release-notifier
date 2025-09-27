import logging

from app.core.config import settings
from motor import motor_asyncio

logging.info(settings)


client = motor_asyncio.AsyncIOMotorClient(
    settings.mongo_uri,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    retryWrites=True,
    w="majority",
    replicaSet=None
)

db = client.get_database(settings.database_name)
