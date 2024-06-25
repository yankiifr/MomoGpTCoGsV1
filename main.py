import discord
from discord.ext import commands
import asyncio
import os
import logging
import random
from config import DISCORD_TOKEN, AVAILABLE_MODELS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f"Loaded extension: {filename[:-3]}")
            except Exception as e:
                logger.error(f"Failed to load extension {filename[:-3]}: {str(e)}")

@bot.event
async def on_ready():
    logger.info(f'{bot.user} s\'est connecté à Discord!')
    await load_cogs()
    await bot.get_cog('ModelManagement').select_initial_model()
    await bot.get_cog('General').send_welcome_message()
    bot.loop.create_task(change_status())

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        custom_id = interaction.data["custom_id"]
        await interaction.response.defer(ephemeral=True)

        if custom_id == "chat":
            await bot.get_cog('AIChat').start_chat(interaction)
        elif custom_id == "model":
            await bot.get_cog('ModelManagement').show_models(interaction)
        elif custom_id == "api":
            await bot.get_cog('ModelManagement').show_api_config(interaction)
        elif custom_id == "help":
            await bot.get_cog('General').show_help(interaction)
        elif custom_id == "quota":
            await bot.get_cog('ModelManagement').check_quotas(interaction)
        elif custom_id == "free_models":
            await bot.get_cog('ModelManagement').show_free_models(interaction)
        elif custom_id == "paid_models":
            await bot.get_cog('ModelManagement').show_paid_models(interaction)

async def change_status():
    statuses = [
        "Prêt à flirter 💋",
        "En mode séduction 😘",
        "Cherche l'âme sœur 💘",
        "Expert en câlins virtuels 🤗",
        "Maître des mots doux 💬",
        "En quête d'amour numérique 💻❤️",
        "Spécialiste des émojis coquins 🍑🍆",
        "Docteur ès romance AI 🤖💕"
    ]
    while True:
        await bot.change_presence(activity=discord.Game(name=random.choice(statuses)))
        await asyncio.sleep(300)  # Change le statut toutes les 5 minutes

async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    logger.info("Démarrage du bot")
    asyncio.run(main())
