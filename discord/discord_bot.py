import discord
from discord.ext import commands
import os
import io
from config import TOKEN, CANAL_ID, GUILD_ID
from redis_queue import push_to_queue
from message_handler import handle_message_by_type
from commands.command_router import get_last_command

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
    try:
        print(f"[*] bot logado como {bot.user}")

        await setup_planning(bot, GUILD_ID) 
        await setup_issues(bot, GUILD_ID)
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
    
    
    last_command = await get_last_command(message.author.id)
    print(f"[i] último comando do usuário {message.author.id}: {last_command}")

    payload = {
        "user_id": message.author.id,
        "user_name": str(message.author),
        "channel_id": message.channel.id,
        "content": result,
        "message_id": message.id,
        "command": last_command or "main_agent",
        "type": "mention",
    }

    await push_to_queue("discord_messages", payload)

async def send_text_message(channel_id: int, intro_message: str, generated_content: str, closing_message: str):
    print(f"[i] enviando mensagem para o canal {channel_id}")

    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"[x] canal {channel_id} não encontrado")
        return

    # envia intro, conteúdo gerado (como arquivo) e mensagem de fechamento
    # se intro for maior que 2000 caracteres, evia como md

    # intro
    if intro_message:
        if len(intro_message) > 2000:
            file = discord.File(io.StringIO(intro_message), filename="intro_message.md")
            await channel.send(file=file)
        else:
            await channel.send(intro_message)

    # conteúdo principal
    if generated_content:
        file = discord.File(io.StringIO(generated_content), filename="generated_content.md")
        await channel.send(file=file)

    # fechamento
    if closing_message:
        if len(closing_message) > 2000:
            file = discord.File(io.StringIO(closing_message), filename="closing_message.md")
            await channel.send(file=file)
        else:
            await channel.send(closing_message)


async def run_bot():
    await bot.start(TOKEN)
