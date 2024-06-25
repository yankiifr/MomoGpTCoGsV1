import discord
from discord.ext import commands
from utils.ai_utils import generate_ai_message
from config import USER_API_KEYS

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_chat_state = {}

    async def start_chat(self, interaction: discord.Interaction):
        if interaction.user.id not in USER_API_KEYS:
            await interaction.followup.send("Veuillez d'abord configurer votre clé API avec le bouton API.", ephemeral=True)
        else:
            self.user_chat_state[interaction.user.id] = True
            await interaction.followup.send("Chat démarré. Envoyez vos messages dans le canal. Pour quitter le chat, tapez 'quit'.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.id in self.user_chat_state and self.user_chat_state[message.author.id]:
            if message.content.lower() == 'quit':
                del self.user_chat_state[message.author.id]
                await message.channel.send("Chat terminé. À bientôt !")
                return

            response = await generate_ai_message(message.content, message.author.id)
            await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(AIChat(bot))
