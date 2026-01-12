import discord
from discord.ext import commands
import os
import io
from dotenv import load_dotenv
from config import TOKEN, CANAL_ID
from redis_queue import push_to_queue
from message_handler import handle_message_by_type

load_dotenv()

GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# carregando comandos
from commands.generate_planning import setup as setup_planning
from commands.generate_issues import setup as setup_issues

@bot.event
async def on_ready():
    print(f"[*] bot logado como {bot.user}")

    await setup_planning(bot, GUILD_ID) 
    await setup_issues(bot, GUILD_ID)

    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"[*] slash commands sincronizados na guild: {len(synced)}")

        canal = await bot.fetch_channel(CANAL_ID)
        await canal.send("bot iniciado e pronto para usar")

    except Exception as e:
        print(f"[x] erro no on_ready: {e}")

# menções

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user not in message.mentions:
        return

    try:
        result = await handle_message_by_type(message)
    except ValueError as e:
        # conteúdo não suportado
        await message.channel.send(
            "Desculpe, aceito apenas mensagens de texto ou arquivos .txt e .md"
        )
        return

    payload = {
        "author_id": message.author.id,
        "author_name": str(message.author),
        "channel_id": message.channel.id,
        "content": result,
        "message_id": message.id,
    }

    await push_to_queue("discord_messages", payload)

async def send_text_message(channel_id: int, content: str):
    print(f"[i] enviando mensagem para o canal {channel_id}")

    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"[x] canal {channel_id} não encontrado")
        return

    # mensagem pequena
    if len(content) <= 2000:
        await channel.send(content)
        return

    # mensagem grande - arquivo .md
    print("[i] mensagem muito longa, enviando como arquivo")
    buffer = io.BytesIO(content.encode("utf-8"))
    file = discord.File(fp=buffer, filename="resposta.md")

    await channel.send(
        content="resposta muito longa, enviada como arquivo:",
        file=file
    )

async def run_bot():
    await bot.start(TOKEN)
