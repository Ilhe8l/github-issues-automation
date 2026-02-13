import asyncio
import discord

# dicionário para rastrear tarefas de "digitando"
typing_tasks = {}

async def typing_loop(channel):
    # mantém o status 'digitando...' ativo no canal
    try:
        while True:
            await channel.typing()
            await asyncio.sleep(8)  # typing() dura aprox 10s, renova a cada 8s
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"[x] erro no loop de typing: {e}")

async def start_typing(client, channel_id: int):
    # inicia o indicador de digitando para um canal
    if channel_id in typing_tasks:
        return # já está digitando

    channel = client.get_channel(channel_id)
    if channel:
        task = asyncio.create_task(typing_loop(channel))
        typing_tasks[channel_id] = task
        print(f"[i] typing iniciado para canal {channel_id}")

async def stop_typing(channel_id: int):
    # para o indicador de digitando para um canal
    if channel_id in typing_tasks:
        typing_tasks[channel_id].cancel()
        del typing_tasks[channel_id]
        print(f"[i] typing parado para canal {channel_id}")
