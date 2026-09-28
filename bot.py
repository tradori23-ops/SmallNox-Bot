import os
import discord
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    raise SystemExit(
        "DISCORD_TOKEN non impostato. Su Railway: Variables -> New Variable -> "
        "DISCORD_TOKEN = <il tuo token>."
    )

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
    print(f"SmallNox e' ONLINE come {bot.user}")
    await bot.change_presence(
        activity=discord.Game(name="LuxComics & MedusaComics")
    )


@bot.tree.command(name="help", description="Show the SmallNox help menu.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="\u2728 SmallNox \u2014 Help",
        description=(
            "Official assistant for LuxComics & MedusaComics.\n\n"
            "\U0001F4DA `/comics` \u2014 Comics information\n"
            "\U0001F3AD `/roleplay` \u2014 RolePlay guide\n"
            "\U0001F3B5 `/music` \u2014 Luxtify information\n"
            "\U0001F310 `/site` \u2014 Official website"
        ),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="site", description="Open the LuxComics & MedusaComics website.")
async def site(interaction: discord.Interaction):
    await interaction.response.send_message("\U0001F310 https://noxmorningstar.com/")


@bot.tree.command(name="roleplay", description="Show the basic RolePlay rules.")
async def roleplay(interaction: discord.Interaction):
    await interaction.response.send_message(
        "\U0001F3AD **RolePlay:** control only your character, respect turns, "
        "avoid godmodding and metagaming, and always respect consent."
    )


@bot.tree.command(name="comics", description="Information about LuxComics & MedusaComics.")
async def comics(interaction: discord.Interaction):
    await interaction.response.send_message(
        "\U0001F4DA Discover comics, artbooks and new releases at https://noxmorningstar.com/"
    )


@bot.tree.command(name="music", description="Information about Luxtify.")
async def music(interaction: discord.Interaction):
    await interaction.response.send_message(
        "\U0001F3B5 **Luxtify** is the music area of LuxComics & MedusaComics."
    )


bot.run(TOKEN)
