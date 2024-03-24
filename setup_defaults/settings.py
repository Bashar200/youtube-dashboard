from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MONGODB_URL = getenv("MONGODB_URL")
