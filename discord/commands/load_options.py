# carrega json para choices do discord com squads pelo redis
import redis.asyncio as redis
from discord import app_commands
from config import REDIS_URL
from commands.command_router import get_redis

import json
from discord import app_commands
from commands.command_router import get_redis

async def load_squad_options():
    redis = await get_redis()
    keys = await redis.keys("squad:*")

    choices: list[app_commands.Choice[str]] = []

    for key in keys:
        raw = await redis.get(key)
        if not raw:
            continue

        squad = json.loads(raw)

        choices.append(
            app_commands.Choice(
                name=squad.get("display_name", squad["id"]),
                value=squad["id"],
            )
        )

    return choices
