# gerencia a rota dos comandos do discord
# se um usuário mandou um comando, ele pode continuar coinversando com o bot via menções
# cada comando representa um agente diferente, e consequemente, um contexto diferente
# então, precisamos mapear o usuário + último comando para um agente específico
# salva no redis user id e last command

import redis.asyncio as redis
from config import REDIS_URL

redis_client = None

async def set_last_command(user_id: int, command: str):
    redis_client = await get_redis()
    await redis_client.hset(f"user:{user_id}", "last_command", command)

async def get_last_command(user_id: int) -> str | None:
    redis_client = await get_redis()
    command = await redis_client.hget(f"user:{user_id}", "last_command")
    return command

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client