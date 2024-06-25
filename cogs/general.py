import discord
from discord.ext import commands
from utils.ai_utils import generate_ai_message
from utils.discord_utils import create_embed, MainView
import pyfiglet
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_welcome_message(self):
        fonts = ["slant", "banner3-D", "isometric1", "block", "digital"]
        chosen_font = random.choice(fonts)
        ascii_art = pyfiglet.figlet_format("MomoGPT", font=chosen_font)

        welcome_prompts = [
            "Tu es MomoGPT, un bot Discord coquin et drôle. Donne un message d'accueil court et suggestif en français, sans être vulgaire.",
            "En tant que MomoGPT, le bot Discord le plus séduisant, écris un message d'accueil qui fait rougir mais reste élégant.",
            "Imagine que tu es MomoGPT, un bot Discord qui flirte subtilement. Crée un message d'accueil qui titille l'imagination sans choquer.",
            "Tu es MomoGPT, le bot Discord qui sait parler d'amour. Compose un message d'accueil romantique et légèrement osé.",
            "En tant que MomoGPT, expert en jeux de mots coquins, écris un message d'accueil plein de double sens amusants."
        ]

        welcome_message = await generate_ai_message(random.choice(welcome_prompts), use_free_model=True)

        for guild in self.bot.guilds:
            if guild.system_channel:
                welcome_embed = create_embed("👋 Bienvenue sur MomoGPT !", f"```\n{ascii_art}\n```\n{welcome_message}", discord.Color.random())
                await guild.system_channel.send(embed=welcome_embed)
                await guild.system_channel.send("Que puis-je faire pour vous aujourd'hui ?", view=MainView())

    async def show_help(self, interaction: discord.Interaction):
        help_embed = create_embed(
            "Aide MomoGPT",
            "Voici quelques conseils pour utiliser MomoGPT :\n\n"
            "**Chat** : Cliquez sur le bouton Chat pour entrer en mode conversation avec le bot.\n"
            "**Modèle** : Choisissez entre les modèles gratuits et payants.\n"
            "**API** : Configurez votre clé API pour utiliser les modèles payants.\n"
            "**Quota** : Vérifiez les quotas des modèles disponibles.\n"
            "Pour quitter le mode chat, tapez 'quit'.\n\n"
            "Pour toute question supplémentaire, n'hésitez pas à contacter l'administrateur.",
            discord.Color.blue()
        )
        await interaction.followup.send(embed=help_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(General(bot))
