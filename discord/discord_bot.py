import discord
from discord.ext import commands
from discord import app_commands
from redis_queue import push_to_queue
from message_handler import handle_message_by_type
from config import TOKEN, CANAL_ID

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logado como {bot.user}")
    
    try:
        canal = await bot.fetch_channel(CANAL_ID)
        await canal.send("Bot iniciado e pronto para usar!")
    except Exception as e:
        print(f"Erro ao enviar mensagem de inicialização: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return    
    
    if bot.user not in message.mentions:
        return        return

    
    result = await handle_message_by_type(message)
    payload = {
        "author_id": message.author.id,
        "author_name": str(message.author),
        "channel_id": message.channel.id,
        #"channel_type": str(message.channel.type),
        "content": result,
        "message_id": message.id,
    }

    await push_to_queue("discord_messages", payload)
    print("Mensagem enviada para a fila Redis.")

async def send_text_message(channel_id: int, content: str):
    print(f"Enviando mensagem para o canal {channel_id}: {content}")
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(content)
    else:
        print(f"Canal {channel_id} não encontrado.")

async def run_bot():
    await bot.start(TOKEN)