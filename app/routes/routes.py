from fastapi import APIRouter, Body, Header, Query, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database, get_redis
ltr_route = APIRouter()


@ltr_route.post("/create")
async def create_dashboard(db: AsyncIOMotorDatabase = Depends(get_database),
                           redis_client = Depends(get_redis)):
    logger.info("/create.routes")
    collection = db["dashboard"]
    result = await collection.insert_one({"hello":"1"})
    res = await redis_client.set("hello", "world")
    return JSONResponse(status_code=status.HTTP_201_CREATED , content={"message":"api working!", "data":None, "success":True})