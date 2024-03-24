import asyncio
import logging

from motor.motor_asyncio import AsyncIOMotorClient
from settings import MONGODB_URL

logger = logging.getLogger(__name__)


async def setup_default_conditions():
    """_summary_: This function will setup indexes and insert few api keys for reuse , this will run at start once and exit"""
    client = AsyncIOMotorClient(MONGODB_URL)
    youtube_details = client["dashboard"]["youtube-details"]
    api_keys = client["dashboard"]["api-keys"]
    pre_generated_keys = [
        "AIzaSyDvODpRwzPqpbsizh-9gXckOdSGW89SR1Y",
        "AIzaSyCjhW51ciuyYJPBopEXmVkRJSuAk3x8phs",
        "AIzaSyDXqzIOG8StsiV1KH0SJhg58jQ94frKTNc",
        "AIzaSyCsQUaI2_tfq1maFFzBIcHsLSWhsaRCkXw",
    ]
    try:
        # Save few keys on the database
        for key in pre_generated_keys:
            await api_keys.update_one(
                filter={
                    "key": key,
                },
                update={"$set": {"active": True, "key": key}},
                upsert=True,
            )
    except Exception as e:
        logger.error(f"[1] - {e}")

    try:
        # Create Index on api-keys collection
        await api_keys.create_index("key", unique=True)
    except Exception as e:
        logger.error(f"[2] - {e}")

    try:
        # Create Index on api-keys collection
        await youtube_details.create_index(["video_id", "channel_id"], unique=True)
    except Exception:
        logger.error(f"[3] - {e}")


async def main():
    await setup_default_conditions()
    logger.info("default configuration successfull!")


if __name__ == "__main__":
    asyncio.run(main())
