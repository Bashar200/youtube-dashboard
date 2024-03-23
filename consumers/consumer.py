import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from dateutil.parser import parse
from motor.motor_asyncio import AsyncIOMotorClient
from settings import DATA_GENERATOR_KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVER, MONGODB_URL

logger = logging.getLogger(__name__)


async def consume():
    consumer = AIOKafkaConsumer(
        DATA_GENERATOR_KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
        group_id="youtube-dashboard-service-group-8",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    await consumer.start()
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client["dashboard"]
        logger.info("Payload Insertion Consumer Started............")
        async for message in consumer:
            try:
                youtube_details = database["youtube-details"]
                value = json.loads(message.value.decode("utf-8"))
                insert_payload = {
                    "title": value.get("snippet").get("title"),
                    "description": value.get("snippet").get("description"),
                    "video_id": value.get("id").get("videoId"),
                    "channel_id": value.get("snippet").get("channelId"),
                    "publish_time": parse(value.get("snippet").get("publishTime")),
                    "thumbnails": value.get("snippet").get("thumbnails"),
                }
                await youtube_details.update_one(
                    filter={
                        "video_id": insert_payload["video_id"],
                        "channel_id": insert_payload["channel_id"],
                    },
                    update={"$set": insert_payload},
                    upsert=True,
                )
            except Exception as e:
                logger.error(f"failed to insert data to db :: {e}")
    finally:
        await consumer.stop()


async def main():
    await consume()


if __name__ == "__main__":
    asyncio.run(main())
