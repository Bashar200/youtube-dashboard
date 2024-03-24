from aiokafka import AIOKafkaProducer

from app.settings import KAFKA_BOOTSTRAP_SERVER


async def init_producer():
    """producer client initiation

    Returns:
        _type_: producer object
    """
    try:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)
        await producer.start()
        return producer
    except Exception as e:
        await producer.stop()
        exit()