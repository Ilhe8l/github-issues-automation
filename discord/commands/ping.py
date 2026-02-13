import discord
import logging

async def setup(bot):
    
    @bot.tree.command(
        name="ping",
        description="Verifica a latência do bot"
    )
    async def ping(interaction: discord.Interaction):
        print(f"[PING] Comando chamado por {interaction.user} ({interaction.user.id})")
        
        try:
            await interaction.response.defer(ephemeral=True)

            latency = interaction.client.latency
            latency_ms = (
                "N/A"
                if latency is None or latency != latency
                else f"{round(latency * 1000)}ms"
            )

            await interaction.followup.send(f"Pong! 🏓 {latency_ms}")

        except Exception as e:
            logging.exception("Erro no comando ping")

            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "Erro ao executar ping.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "Erro ao executar ping.",
                    ephemeral=True
                )
