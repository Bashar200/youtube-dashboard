from dotenv import find_dotenv, load_dotenv
from os import getenv
load_dotenv(find_dotenv())

BASE_ROUTE = getenv("BASE_ROUTE")
ENV = getenv("ENV")
LOG_LEVEL= getenv("LOG_LEVEL")
SERVICE_NAME= getenv("SERVICE_NAME")
MONGODB_URL=getenv("MONGODB_URL")