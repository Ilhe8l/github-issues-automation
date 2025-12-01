import redis.asyncio as redis
import json

redis_cliendt = None

async def get_redis():
    global redis_cliendt
    if redis_cliendt is None:
        redis_cliendt = redis.from_url("redis://redis:6379", decode_responses=True)
    return redis_cliendt

async def push_to_queue(queue_name: str, data: dict) -> bool:
    # adiciona mensagem na fila Redis com correlation_id
    try:
        client = await get_redis()
        # Garante que sempre tem correlation_id
        #if "correlation_id" not in data:
        #    data["correlation_id"] = str(uuid.uuid4())
        print(f"Adicionando na fila {queue_name} a mensagem: {data}")
        message = json.dumps(data, ensure_ascii=False)
        await client.lpush(queue_name, message)
        print(f"Mensagem adicionada na fila {queue_name}")
        #logger.info(f"Mensagem adicionada na fila {queue_name} - correlation_id: {data['correlation_id']}")
        return True
    except Exception as e:
        #logger.error(f"Erro Redis: {e}")
        return False