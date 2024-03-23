import logging
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.routes.routes import ltr_route
from app.settings import *

extra = {"app_name": SERVICE_NAME}
logging.basicConfig(level=LOG_LEVEL, format=f'%(asctime)s - {SERVICE_NAME}:- %(levelname)s - %(funcName)s - %(message)s')
logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(logger, extra)
app = FastAPI()
logger.info(f"{SERVICE_NAME} SERVICE STARTED......")


app.include_router(ltr_route, tags=["ltr-dashboard"], prefix=f"{BASE_ROUTE}/v1")


@app.get(f"{BASE_ROUTE}/public/healthz", tags=["Root"])
async def health_check():
    return {"message": "OK"}


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(request, exc):
    if isinstance((exc), (ValidationError)):
        response_dict = {
            "success": False,
            "message": f"{exc.errors()[0].get('loc')[1]} | {exc.errors()[0].get('msg')}",
            "data": None
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response_dict)