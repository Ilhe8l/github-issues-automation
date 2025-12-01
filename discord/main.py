import asyncio
from discord_bot import run_bot
from consumer import consume_responses

async def main():
    print("Discord main started...")
    consumer_task = asyncio.create_task(consume_responses())

    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())