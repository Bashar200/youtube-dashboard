import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager

import googleapiclient.discovery
import pytz
from aiokafka import AIOKafkaProducer
from dateutil.parser import parse
from fastapi import FastAPI
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from app.database import get_database
from app.producer import init_producer
from app.settings import DATA_GENERATOR_KAFKA_TOPIC, GOOGLE_API_KEY

logger = logging.getLogger(__name__)


async def fetch_new_api_key_and_update_old_keys(developer_key):
    database = await get_database()
    collection = database["api-keys"]
    await collection.update_one(
        filter={
            "key": developer_key,
        },
        update={"$set": {"last_active": datetime.now(), "key":developer_key, "active": False}},
        upsert=True
    )
    await collection.update_many(
        filter={
            "last_active": {"$lt": datetime.now() - timedelta(hours=24)},
        },
        update={"$set": {"active": True}}
    )
    res = await collection.find({"active": True}).to_list(None)
    if not res:
        logger.warning("api keys exhausted!! add/create new keys or wait for oldest key to replenish")
    return res[0] if res else []
    


async def gather_information(
    query: str, max_results: int = 10, developer_key=GOOGLE_API_KEY
) -> tuple:
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=developer_key
    )
    published_after = parse("2023-01-01")
    utc_timezone = pytz.utc
    published_after = published_after.astimezone(utc_timezone).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    search_response = {}
    try:
        search_response = (
            youtube.search()
            .list(
                q=query,
                part="id, snippet",
                maxResults=max_results,
                type="video",
                order="date",
                publishedAfter=published_after,
            )
            .execute()
        )
    except HttpError as e:
        logger.error(f"{e.reason}")
        return False, {}
    return True, search_response.get("items")


async def produce_data_to_extractor_stream(data: dict, producer: AIOKafkaProducer):
    await producer.send(
        DATA_GENERATOR_KAFKA_TOPIC, value=json.dumps(data).encode("utf-8")
    )


async def fetch_and_save_youtube_videos_metadata():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    producer = await init_producer()
    developer_key = GOOGLE_API_KEY
    while True:
        success, data = await gather_information(
            "world news", developer_key=developer_key
        )
        if data and success:
            raw_stream_data = [
                produce_data_to_extractor_stream(record, producer) for record in data
            ]
            await asyncio.gather(*raw_stream_data)
        if not success:
            new_api_key = await fetch_new_api_key_and_update_old_keys(developer_key)
            developer_key = new_api_key.get("key") if new_api_key else developer_key 

        await asyncio.sleep(100)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(
        fetch_and_save_youtube_videos_metadata(), name="gather_youtube_data"
    )
    yield
