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
    """_summary_

    Args:
        db (AsyncIOMotorDatabase, optional): database context for GET API data aggregation. Defaults to Depends(get_database).
        redis_client (_type_, optional): redis_client for caching. Defaults to Depends(get_redis).
        search (str, optional): search parameter. Defaults to Query(None, min_length=1).
        page (int, optional): current page for pagination. Defaults to 1.
        page_size (int, optional): total records on a single page. Defaults to 10.

    Returns:
        _type_: JSONResponse
        returns: json reponse data with youtube content
    """
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
