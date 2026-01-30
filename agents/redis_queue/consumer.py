from redis import asyncio as aioredis 
from send_message import process_message 
import json
import asyncio
from config import REDIS_URL
import logging
from stateTypes import State
redis_client = None
# limite de tarefas simultaneas 
MAX_CONCURRENT_TASKS = 1

semaforo = asyncio.Semaphore(MAX_CONCURRENT_TASKS) 

async def consumer(tarefa: str): 
    async with semaforo:  # garante limite 
        logging.info(f"[START] {tarefa}") 
        
        # parse do json para extrair dados
        task_data = json.loads(tarefa)
        session_id = task_data.get("channel_id")
        user_id = task_data.get("user_id")
        mensagem = task_data.get("content")
        channel_id = task_data.get("channel_id")
        command = task_data.get("command", "main_agent")  # comando padrão
        squad_id = None
        if "squad" in task_data:
            squad_id = task_data["squad"]
            logging.info(f"Squad ID definido para: {squad_id}")

        print(f"Processando mensagem para session_id: {session_id}, user_id: {user_id}, mensagem: {mensagem}")

        try:
            #chama o process_message e aguarda o resultado
            result = await process_message(mensagem, session_id, user_id, squad_id,command)

            response = {
                "status": "success",
                "response": result["response"], 
                "session_id": session_id,
                "user_id": user_id,
                "channel_id": channel_id,
                #"timestamp": datetime.now().isoformat(),
                #"processed": False  # Flag para controle
            }
            await redis_client.lpush("discord_messages_response", json.dumps(response))

        
        except Exception as e:
            error_response = {
                "status": "error",
                "message": str(e),
            }
            await redis_client.set(user_id, json.dumps(error_response), ex=1800)  # Armazena o erro com TTL de meia hora
            response = {
                "status": "error",
                "response": "*Opa!* Ocorreu um pequeno erro ao processar sua solicitação. Por favor, tente novamente mais tarde.",
                "channel_id": channel_id,
                "session_id": session_id,
                "user_id": user_id,
            }
            print(error_response, command)
            await redis_client.lpush("discord_messages_response", json.dumps(response)),               
            
async def initConsumer(): 
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
    logging.info("Consumidor iniciado...") 
    
    while True: 
        fila, tarefa = await redis_client.blpop("discord_messages") 
        logging.info(f"Nova tarefa recebida na fila {fila}: {tarefa}")
        # lança a task concorrente, mas respeitando o semáforo 
        asyncio.create_task(consumer(tarefa)) 

#asyncio.run(initConsumer())