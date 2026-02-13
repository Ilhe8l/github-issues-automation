import discord
from discord import app_commands
from redis_queue import push_to_queue
from commands.command_router import set_last_command
from commands.load_options import load_squad_options
from typing_utils import start_typing

async def setup(bot, GUILD_ID):
    squad_choices = await load_squad_options()

    @bot.tree.command(
        name="issues_agent",
        description="Gera issues a partir de um planning ou mensagem",
        guild=discord.Object(id=GUILD_ID)
    )
    @app_commands.describe(
        squad="Squad responsável pelo planejamento",
        planning_file="Arquivo .txt ou .md com o planning (opcional)",
        extra_file="Arquivo extra para contexto adicional (opcional)",
        message=(
            "Mensagem opcional para complementar o planning "
            "ou enviar instruções adicionais ao bot"
        )
    )
    @app_commands.choices(squad=squad_choices)
    async def generate_issues(
        interaction: discord.Interaction, 
        squad: str,
        planning_file: discord.Attachment | None = None,
        extra_file: discord.Attachment | None = None,
        message: str | None = None
    ):
        await interaction.response.defer(ephemeral=True)

        # precisa ter pelo menos arquivo ou mensagem
        if planning_file is None and not message:
            await interaction.followup.send(
                "Você precisa enviar um arquivo (.txt/.md) ou escrever uma mensagem.",
                ephemeral=True
            )
            return

        content_parts: list[str] = []

        if planning_file:
            file_bytes = await planning_file.read()
            content_parts.append(file_bytes.decode("utf-8"))

        if extra_file:
            file_bytes = await extra_file.read()
            content_parts.append(f"\n\n[arquivo extra: {extra_file.filename}]\n" + file_bytes.decode("utf-8"))

        if message:
            content_parts.append(
                "\n\n---\n\n"
                "## Mensagem adicional do usuário\n\n"
                f"{message}"
            )

        content = "".join(content_parts)

        command = "generate_issues"
        await set_last_command(interaction.user.id, command)

        print(content)

        payload = {
            "type": "slash_command",
            "command": command,
            "user_id": interaction.user.id,
            "user_name": str(interaction.user),
            "channel_id": interaction.channel_id,
            "guild_id": interaction.guild_id,
            "content": content,
            "interaction_id": interaction.id,
            "squad": squad,
        }

        await push_to_queue("discord_messages", payload)

        await interaction.followup.send(
            f"Solicitação de issues enviada para o squad **{squad}**. "
            "Você receberá uma mensagem quando estiver pronto."
        )
        
        await start_typing(interaction.client, interaction.channel_id)
