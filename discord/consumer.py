import asyncio
import json
import redis.asyncio as redis
import logging
from discord_bot import send_text_message
from config import REDIS_URL

redis_client = None

async def consume_responses():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    print("Consumer de respostas iniciado...")
    while True:
        try:
            # brpop bloqueia até ter mensagem
            _, raw_data = await redis_client.brpop("discord_messages_response")
            print(f"Mensagem recebida na fila de respostas: {raw_data}")
            
            data = json.loads(raw_data) 

            #correlation_id = data.get("correlation_id")
            #to_number = data.get("user_id")
            message = data.get("response")
            channel_id = data.get("channel_id")
            print(f"Enviando mensagem para o canal {channel_id}: {message}")
            await send_text_message(channel_id, message)
                        
           

            # envia mensagem pelo WhatsApp
            
            #logger.info(f"Enviado para {to_number} (corr_id={correlation_id}) -> {message}")

        except Exception as e:
            #logger.error(f"Erro no consumer: {e}", exc_info=True)
            await asyncio.sleep(2)  # evita crash loop

if __name__ == "__main__":
    asyncio.run(consume_responses())
