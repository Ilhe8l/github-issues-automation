import redis.asyncio as redis
import json
from config import REDIS_URL

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client

async def push_to_queue(queue_name: str, data: dict) -> bool:
    # adiciona mensagem na fila redis
    try:
        client = await get_redis()
        print(f"[i] adicionando na fila {queue_name} a mensagem: {data}")
        message = json.dumps(data, ensure_ascii=False)
        await client.lpush(queue_name, message)
        print(f"[*] mensagem adicionada na fila {queue_name}")
        return True
    except Exception as e:
        print(f"[x] erro redis: {e}")
        return False