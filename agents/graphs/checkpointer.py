from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from config import REDIS_URL, TTL_CONFIG

_checkpointer: AsyncRedisSaver | None = None

async def get_checkpointer() -> AsyncRedisSaver:
    global _checkpointer

    if _checkpointer is None:
        _checkpointer = AsyncRedisSaver(
            redis_url=REDIS_URL,
            ttl=TTL_CONFIG,
        )
        await _checkpointer.asetup()

    return _checkpointer
