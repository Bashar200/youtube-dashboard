from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_ROUTE = getenv("BASE_ROUTE")
ENV = getenv("ENV")
LOG_LEVEL = getenv("LOG_LEVEL")
SERVICE_NAME = getenv("SERVICE_NAME")
MONGODB_URL = getenv("MONGODB_URL")
GOOGLE_API_KEY = getenv("GOOGLE_API_KEY")
KAFKA_BOOTSTRAP_SERVER = getenv("KAFKA_BOOTSTRAP_SERVER")
DATA_GENERATOR_KAFKA_TOPIC = getenv("DATA_GENERATOR_KAFKA_TOPIC")
