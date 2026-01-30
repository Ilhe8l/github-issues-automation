import json
from services.redis import get_redis_client

async def get_squad_info(squad_id: str) -> dict:
    redis_client = get_redis_client()
    raw = await redis_client.get(f"squad:{squad_id}")
    if not raw:
        raise ValueError(f"Squad com ID {squad_id} não encontrada no Redis.")
    return json.loads(raw)
