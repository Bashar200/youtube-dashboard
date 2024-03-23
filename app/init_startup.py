import asyncio
import logging
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from dateutil.parser import parse
import pytz
import json
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from app.producer import init_producer
from app.settings import DATA_GENERATOR_KAFKA_TOPIC, GOOGLE_API_KEY
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)


async def gather_information(query: str, max_results: int = 10) -> list:
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=GOOGLE_API_KEY
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
    return search_response.get("items")


async def produce_data_to_extractor_stream(data: dict, producer: AIOKafkaProducer):
    await producer.send(
        DATA_GENERATOR_KAFKA_TOPIC, value=json.dumps(data).encode("utf-8")
    )


async def fetch_and_save_youtube_videos_metadata():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    producer = await init_producer()
    while True:
        data = await gather_information("world news")
        if data:
            raw_stream_data = [
                produce_data_to_extractor_stream(record, producer) for record in data
            ]
            await asyncio.gather(*raw_stream_data)

        await asyncio.sleep(500)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(
        fetch_and_save_youtube_videos_metadata(), name="gather_youtube_data"
    )
    yield
