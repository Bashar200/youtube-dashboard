import logging

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.init_startup import lifespan
from app.routes.routes import route
from app.settings import *

extra = {"app_name": SERVICE_NAME}
logger = logging.getLogger(__name__)
app = FastAPI(lifespan=lifespan)

# app = FastAPI()

app.include_router(route, tags=["version 1.0"], prefix=f"{BASE_ROUTE}/v1")


@app.get(f"{BASE_ROUTE}/public/healthz", tags=["Root"])
async def health_check():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "OK"})


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(request, exc):
    response_dict = {
        "success": False,
        "message": f"{exc.errors()[0].get('loc')[1]} | {exc.errors()[0].get('msg')}",
        "data": None,
    }
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response_dict)
