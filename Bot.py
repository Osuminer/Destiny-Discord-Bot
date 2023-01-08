from keys import DISCORD_API_TOKEN, BUNGIE_API_TOKEN
import PyDest
import os
import discord
from discord import app_commands, interactions
from discord.ext import tasks, commands
import pprint

# Constants
TOP_MODIFIERS = ['Shielded Foes', 'Champion Foes', 'Double Nightfall Drops', 'Ashes to Ashes', 'Lightning Crystals',
                 'Acute Arc Burn', 'Match Game', 'Champions: Mob', 'Attrition']

# Setup discord bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# Setup pydest api wrapper
destiny = PyDest.PyDest(BUNGIE_API_TOKEN)
# HEADERS = {"X-API-Key": BUNGIE_API_TOKEN}

@bot.event
async def setup_hook():
	# Load all cogs
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await bot.load_extension(f'cogs.{filename[:-3]}')
			print(f'Loaded {filename}')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected')

    # Sync commands with Discord on bot startup
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands\n")
    except Exception as e:
        print(e)


# Print Membership Id
@bot.tree.command(name="getmemid")
@app_commands.describe(bungie_id="Enter your bungie id")
async def GetPlayer(interaction: discord.Interaction, bungie_id: str):

    player = destiny.api.search_destiny_player(1, bungie_id)
    memId = player['Response'][0]['membershipId']

    print(f"{interaction.user.name}, your membership id is {memId}")
    await interaction.response.send_message(f"{interaction.user.name}, your membership id is {memId}", ephemeral=True)


bot.run(DISCORD_API_TOKEN)
