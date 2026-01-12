import discord
from discord import app_commands
from redis_queue import push_to_queue

async def setup(bot, GUILD_ID):

    @bot.tree.command(
        name="generate_planning",
        description="Gera um planejamento a partir de um backlog",
        guild=discord.Object(id=GUILD_ID)
    )
    @app_commands.describe(
        backlog_file="Arquivo .txt ou .md com o backlog"
    )
    async def generate_planning(
        interaction: discord.Interaction,
        backlog_file: discord.Attachment
    ):
        await interaction.response.defer(ephemeral=True)
        content = await backlog_file.read()
        backlog_text = content.decode("utf-8")
        payload = {
            "type": "slash_command",
            "command": "generate_planning",
            "author_id": interaction.user.id,
            "author_name": str(interaction.user),
            "channel_id": interaction.channel_id,
            "guild_id": interaction.guild_id,
            "content": backlog_text,
            "interaction_id": interaction.id,
        }

        await push_to_queue("discord_messages", payload)

        await interaction.followup.send(
            "Planejamento enviado para processamento. Você receberá uma mensagem quando estiver pronto"
        )
