import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.settings import *

client = AsyncIOMotorClient(MONGODB_URL)
database = client["dashboard"]
redis_client = redis.Redis()


async def get_database() -> AsyncIOMotorDatabase:
    """get context of Mongo database

    Returns:
        AsyncIOMotorDatabase
    """
    return database


async def get_redis() -> redis.Redis:
    """get context of Redis database

    Returns:
        redis.Redis
    """
    return redis_client
