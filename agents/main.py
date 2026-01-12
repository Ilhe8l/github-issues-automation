import asyncio
from graphs.router_graph import get_router_graph
from redis_queue.consumer import initConsumer
from graphs.checkpointer import get_checkpointer
async def main():
    checkpointer = await get_checkpointer()
    await checkpointer.asetup()

    await get_router_graph(checkpointer)

    consumer_task = asyncio.create_task(initConsumer())
    await consumer_task

if __name__ == "__main__":
    asyncio.run(main())