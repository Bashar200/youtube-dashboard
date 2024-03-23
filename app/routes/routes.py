from fastapi import APIRouter, Body, Depends, Header, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database, get_redis
from app.services.services import get_youtube_contents

route = APIRouter()


@route.get("/get/contents")
async def create_dashboard(
    db: AsyncIOMotorDatabase = Depends(get_database),
    redis_client=Depends(get_redis),
    search: str = Query(None, min_length=1),
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
):
    logger.info("/create.routes")
    res = await get_youtube_contents(
        db, redis_client, search, page=page, page_size=page_size
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "data": res,
            "message": "successfully fetch youtube content data",
            "success": True,
        },
    )
