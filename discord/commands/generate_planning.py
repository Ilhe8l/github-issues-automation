import json
import discord
from discord import app_commands

from redis_queue import push_to_queue
from commands.command_router import set_last_command
from commands.load_options import load_squad_options

# setup do comando

async def setup(bot, GUILD_ID):
    squad_choices = await load_squad_options()

    @bot.tree.command(
        name="planning_agent",
        description="Gera um planejamento a partir de um backlog ou mensagem",
        guild=discord.Object(id=GUILD_ID),
    )
    @app_commands.describe(
        squad="Squad responsável pelo planejamento",
        backlog_file="Arquivo .txt ou .md com o backlog (opcional)",
        message=(
            "Mensagem opcional para complementar o backlog "
            "ou enviar instruções adicionais ao bot"
        ),
    )
    @app_commands.choices(squad=squad_choices)
    async def generate_planning(
        interaction: discord.Interaction,
        squad: str,  
        backlog_file: discord.Attachment | None = None, 
        message: str | None = None,
    ):
        await interaction.response.defer(ephemeral=True)

        # precisa ter pelo menos arquivo ou mensagem
        if backlog_file is None and not message:
            await interaction.followup.send(
                "Você precisa enviar um arquivo (.txt/.md) ou escrever uma mensagem.",
                ephemeral=True,
            )
            return

        content_parts: list[str] = []

        if backlog_file:
            file_bytes = await backlog_file.read()
            content_parts.append(file_bytes.decode("utf-8"))

        if message:
            content_parts.append(
                "\n\n---\n\n"
                "## Mensagem adicional do usuário\n\n"
                f"{message}"
            )

        content = "".join(content_parts)

        command = "generate_planning"
        await set_last_command(interaction.user.id, command)

        payload = {
            "type": "slash_command",
            "command": command,
            "user_id": interaction.user.id,
            "user_name": str(interaction.user),
            "channel_id": interaction.channel_id,
            "guild_id": interaction.guild_id,
            "interaction_id": interaction.id,
            "squad": squad,   
            "content": content,
        }

        await push_to_queue("discord_messages", payload)

        await interaction.followup.send(
            f"Planejamento enviado para o squad **{squad}**. "
            "Você receberá uma mensagem quando estiver pronto.",
            ephemeral=True,
        )
