import discord

def create_embed(title, description, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="Powered by MomoGPT")
    return embed

class MainView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Chat", custom_id="chat", style=discord.ButtonStyle.success, emoji="💬"))
        self.add_item(discord.ui.Button(label="Modèle", custom_id="model", style=discord.ButtonStyle.primary, emoji="🤖"))
        self.add_item(discord.ui.Button(label="API", custom_id="api", style=discord.ButtonStyle.secondary, emoji="🔑"))
        self.add_item(discord.ui.Button(label="Aide", custom_id="help", style=discord.ButtonStyle.secondary, emoji="❓"))
        self.add_item(discord.ui.Button(label="Quota", custom_id="quota", style=discord.ButtonStyle.danger, emoji="📊"))
