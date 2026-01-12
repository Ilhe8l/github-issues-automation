import discord
from discord import app_commands
from redis_queue import push_to_queue


async def setup(bot, GUILD_ID):

    @bot.tree.command(
        name="generate_issues",
        description="Gera issues a partir de um planning",
        guild=discord.Object(id=GUILD_ID)
    )
    @app_commands.describe(
        planning_file="Arquivo .txt ou .md com o planning"
    )
    async def generate_issues(
        interaction: discord.Interaction,
        planning_file: discord.Attachment
    ):
        await interaction.response.defer(ephemeral=True)

        content = await planning_file.read()
        planning_text = content.decode("utf-8")

        payload = {
            "type": "slash_command",
            "command": "generate_issues",
            "author_id": interaction.user.id,
            "author_name": str(interaction.user),
            "channel_id": interaction.channel_id,
            "guild_id": interaction.guild_id,
            "content": planning_text,
            "interaction_id": interaction.id,
        }

        await push_to_queue("discord_messages", payload)

        await interaction.followup.send(
            "Planning enviado para geracao de issues. Você receberá uma mensagem quando estiver pronto"
        )
