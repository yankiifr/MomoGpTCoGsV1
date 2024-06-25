import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Commande inconnue.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Il manque un argument requis pour cette commande.")
        else:
            await ctx.send(f"Une erreur s'est produite : {str(error)}")

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))