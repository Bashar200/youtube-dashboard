from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

KAFKA_BOOTSTRAP_SERVER = getenv("KAFKA_BOOTSTRAP_SERVER")
DATA_GENERATOR_KAFKA_TOPIC = getenv("DATA_GENERATOR_KAFKA_TOPIC")
MONGODB_URL = getenv("MONGODB_URL")
