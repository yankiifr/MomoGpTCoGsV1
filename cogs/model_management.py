import discord
from discord.ext import commands
import random
from config import AVAILABLE_MODELS, USER_API_KEYS
from utils.ai_utils import ping_model, encrypt_api_key

class ModelManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model_quotas = {}

    async def select_initial_model(self):
        free_models = []
        for provider, models in AVAILABLE_MODELS["Gratuit"].items():
            free_models.extend(models)

        random.shuffle(free_models)

        for model in free_models:
            if await ping_model(model):
                self.bot.default_model = model
                print(f"Modèle initial sélectionné : {model}")
                return

        print("Aucun modèle gratuit n'a répondu au ping. Utilisation du premier modèle disponible.")
        self.bot.default_model = free_models[0]

    async def show_models(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modèles disponibles", color=discord.Color.blue())

        for category, providers in AVAILABLE_MODELS.items():
            value = ""
            for provider, models in providers.items():
                value += f"**{provider}**: {', '.join(models)}\n"
            embed.add_field(name=category, value=value, inline=False)

        view = ModelSelectionView()
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

    async def show_free_models(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modèles gratuits disponibles", color=discord.Color.green())
        for provider, models in AVAILABLE_MODELS["Gratuit"].items():
            embed.add_field(name=provider, value=", ".join(models), inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def show_paid_models(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modèles payants disponibles", color=discord.Color.blue())
        for provider, models in AVAILABLE_MODELS["Payant"].items():
            embed.add_field(name=provider, value=", ".join(models), inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def show_api_config(self, interaction: discord.Interaction):
        await interaction.followup.send("Veuillez entrer votre clé API en utilisant la commande `!set_api_key <provider> <api_key>`", ephemeral=True)

    @commands.command()
    async def set_api_key(self, ctx, provider: str, api_key: str):
        if ctx.guild is not None:
            await ctx.send("Cette commande ne peut être utilisée qu'en message privé pour des raisons de sécurité.")
            return

        if provider.lower() not in ["openai", "perplexity", "mistral", "codestral"]:
            await ctx.send("Fournisseur non valide. Utilisez 'openai', 'perplexity', 'mistral' ou 'codestral'.")
            return

        encrypted_key = encrypt_api_key(api_key)
        USER_API_KEYS[ctx.author.id] = {provider.lower(): encrypted_key}

        await ctx.send("Votre clé API a été enregistrée avec succès et cryptée pour votre sécurité.")

    async def check_quotas(self, interaction: discord.Interaction):
        quota_info = "Quotas des modèles :\n"
        for category, providers in AVAILABLE_MODELS.items():
            quota_info += f"\n{category}:\n"
            for provider, models in providers.items():
                for model in models:
                    quota = random.randint(0, 100)  # Simuler un quota pour l'exemple
                    quota_info += f"  - {provider} {model}: {quota}%\n"
        await interaction.followup.send(quota_info, ephemeral=True)

class ModelSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Modèles gratuits", custom_id="free_models", style=discord.ButtonStyle.success))
        self.add_item(discord.ui.Button(label="Modèles payants", custom_id="paid_models", style=discord.ButtonStyle.primary))

async def setup(bot):
    await bot.add_cog(ModelManagement(bot))
