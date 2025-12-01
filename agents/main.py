import asyncio
from graph import get_graph
from redis_queue.consumer import initConsumer

async def main():
    consumer_task = asyncio.create_task(initConsumer())
    await get_graph()
    await consumer_task

if __name__ == "__main__":
    asyncio.run(main())