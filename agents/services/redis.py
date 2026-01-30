from redis.asyncio import Redis
from config import REDIS_URL

def get_redis_client() -> Redis:
    """Inicializa e retorna o cliente Redis."""
    return Redis.from_url(REDIS_URL, decode_responses=True) 

