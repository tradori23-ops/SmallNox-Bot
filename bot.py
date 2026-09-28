import os
import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands, tasks

TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    raise SystemExit(
        "DISCORD_TOKEN non impostato. Su Railway: Variables -> New Variable -> "
        "DISCORD_TOKEN = <il tuo token>."
    )

# Canale dove postare buongiorno/buonanotte in automatico. Facoltativo: se non
# e' impostata, il bot parte comunque, solo senza i messaggi automatici (i
# comandi /buongiorno e /buonanotte restano disponibili in ogni caso).
ANNOUNCE_CHANNEL_ID = os.environ.get("ANNOUNCE_CHANNEL_ID")
ANNOUNCE_CHANNEL_ID = int(ANNOUNCE_CHANNEL_ID) if ANNOUNCE_CHANNEL_ID else None

ROME = ZoneInfo("Europe/Rome")
MORNING_MESSAGE = (
    "\u2600\ufe0f **Good morning!** Another day to get lost in the pages of "
    "LuxComics & MedusaComics \u2014 happy reading, everyone! \U0001F4D6"
)
NIGHT_MESSAGE = (
    "\U0001F319 **Good night, everyone** \u2014 may your dreams be as vivid as "
    "the pages of Lucifer, Lilith, Lucifera and Lucio. See you tomorrow! \u2728"
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
    if ANNOUNCE_CHANNEL_ID:
        if not morning_announcement.is_running():
            morning_announcement.start()
        if not night_announcement.is_running():
            night_announcement.start()
        print(f"Messaggi automatici attivi sul canale {ANNOUNCE_CHANNEL_ID}")
    else:
        print("ANNOUNCE_CHANNEL_ID non impostata: solo i comandi /buongiorno e /buonanotte sono attivi, niente automatico.")


@bot.tree.command(name="help", description="Show the SmallNox help menu.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="\u2728 SmallNox \u2014 Help",
        description=(
            "Official assistant for LuxComics & MedusaComics.\n\n"
            "\U0001F4DA `/comics` \u2014 Comics information\n"
            "\U0001F3AD `/roleplay` \u2014 RolePlay guide\n"
            "\U0001F3B5 `/music` \u2014 Luxtify information\n"
            "\U0001F310 `/site` \u2014 Official website\n"
            "\u2600\ufe0f `/goodmorning` \u2014 Good morning message\n"
            "\U0001F319 `/goodnight` \u2014 Good night message"
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


@bot.tree.command(name="goodmorning", description="Send the good morning message.")
async def goodmorning(interaction: discord.Interaction):
    await interaction.response.send_message(MORNING_MESSAGE)


@bot.tree.command(name="goodnight", description="Send the good night message.")
async def goodnight(interaction: discord.Interaction):
    await interaction.response.send_message(NIGHT_MESSAGE)


# Messaggi automatici, un giorno via l'altro, alla stessa ora esatta (ora
# italiana: si aggiusta da sola quando cambia l'ora legale, non serve
# ritoccarla noi due volte l'anno). Partono solo se ANNOUNCE_CHANNEL_ID e'
# impostata; altrimenti restano definite ma ferme, il bot non si rompe.
@tasks.loop(time=datetime.time(hour=8, minute=0, tzinfo=ROME))
async def morning_announcement():
    channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
    if channel:
        await channel.send(MORNING_MESSAGE)


@tasks.loop(time=datetime.time(hour=23, minute=0, tzinfo=ROME))
async def night_announcement():
    channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
    if channel:
        await channel.send(NIGHT_MESSAGE)


bot.run(TOKEN)
