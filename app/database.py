from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.settings import *
import redis.asyncio as redis


client = AsyncIOMotorClient(MONGODB_URL)
database = client["letterdrop"]
redis_client = redis.Redis()


async def get_database() -> AsyncIOMotorDatabase:
    return database

async def get_redis() -> redis.Redis:
    return redis_client

