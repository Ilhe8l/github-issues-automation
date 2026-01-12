import asyncio
import json
import redis.asyncio as redis
from discord_bot import send_text_message
from config import REDIS_URL

redis_client = None

async def consume_responses():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    print("[i] consumer de respostas iniciado")
    while True:
        try:
            # brpop bloqueia até ter mensagem
            _, raw_data = await redis_client.brpop("discord_messages_response")
            print(f"[i] mensagem recebida na fila de respostas: {raw_data}")
            
            data = json.loads(raw_data) 

            message = data.get("response")
            channel_id = data.get("channel_id")
            print(f"[i] enviando mensagem para o canal {channel_id}: {message}")
            await send_text_message(channel_id, message)

        except Exception as e:
            print(f"[x] erro no consumer: {e}")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(consume_responses())
