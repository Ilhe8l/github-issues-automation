from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
TOKEN = os.getenv("DISCORD_TOKEN")
CANAL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))