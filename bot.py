import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Add your bot token to the .env file.")

intents = discord.Intents.default()

class SmallNox(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        synced = await self.tree.sync()
        print(f"Slash commands synced: {len(synced)}")

bot = SmallNox()

@bot.event
async def on_ready():
    print(f"SmallNox is online as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="LuxComics & MedusaComics"))

@bot.tree.command(name="help", description="Show the SmallNox help menu.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✨ SmallNox — Help",
        description=(
            "Official assistant for LuxComics & MedusaComics.\n\n"
            "📚 `/comics` — Comics information\n"
            "🎭 `/roleplay` — RolePlay guide\n"
            "🎵 `/music` — Luxtify information\n"
            "🌐 `/site` — Official website"
        )
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="site", description="Open the LuxComics & MedusaComics website.")
async def site(interaction: discord.Interaction):
    await interaction.response.send_message("🌐 https://noxmorningstar.com/")

@bot.tree.command(name="roleplay", description="Show the basic RolePlay rules.")
async def roleplay(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🎭 **RolePlay:** control only your character, respect turns, "
        "avoid godmodding and metagaming, and always respect consent."
    )

@bot.tree.command(name="comics", description="Information about LuxComics & MedusaComics.")
async def comics(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📚 Discover comics, artbooks and new releases at https://noxmorningstar.com/"
    )

@bot.tree.command(name="music", description="Information about Luxtify.")
async def music(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🎵 **Luxtify** is the music area of LuxComics & MedusaComics."
    )

bot.run(TOKEN)
