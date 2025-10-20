from dotenv import load_dotenv
import os

load_dotenv()  # loads the .env file

print(os.getenv("DATABASE_URL"))  # just to confirm
import asyncio
import json
import logging
from typing import Any, Dict
import aio_pika
import os
from dotenv import load_dotenv
from prisma import Prisma

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Prisma ORM
db = Prisma()

# Queue configuration
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "ai_resume_tasks")


async def process_task(task: Dict[str, Any]):
    """
    Process incoming AI tasks (e.g., resume analysis, fraud re-analysis).
    """
    logger.info(f"Processing task: {task}")

    try:
        task_type = task.get("type")
        resume_id = task.get("resume_id")

        # Example: AI Resume Re-analysis
        if task_type == "reanalyze_resume" and resume_id:
            from ai_consumer.services.resume_ai import reanalyze_resume
            result = await reanalyze_resume(db, resume_id)
            logger.info(f"Re-analysis completed for resume {resume_id}: {result}")
        else:
            logger.warning(f"Unknown or incomplete task received: {task}")

    except Exception as e:
        logger.error(f"Error processing task: {e}", exc_info=True)


async def consume():
    """
    Connects to RabbitMQ and continuously consumes AI tasks from the queue.
    """
    logger.info("Connecting to RabbitMQ...")
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    # Ensure queue exists
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    logger.info(f"Connected to queue: {QUEUE_NAME}")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                task = json.loads(message.body.decode())
                await process_task(task)


async def main():
    """
    Entry point — connects to DB and starts the consumer.
    """
    await db.connect()
    logger.info("✅ AI Consumer connected to Prisma DB")

    await consume()

    await db.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Consumer stopped manually.")
