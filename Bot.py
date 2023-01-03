from keys import DISCORD_API_TOKEN, BUNGIE_API_TOKEN
from PyDest import pydest
import discord
from discord import app_commands
from discord.ext import tasks, commands
import pprint

# Setup discord bot
bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())

# Setup pydest api wrapper
destiny = pydest(BUNGIE_API_TOKEN)
HEADERS = {"X-API-Key":BUNGIE_API_TOKEN}

# Sync commands with Discord on bot startup
@bot.event
async def on_ready():
	print(f'{bot.user} has connected')

	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} commands")
	except Exception as e:
		print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
	await interaction.response.send_message(f'Hey {interaction.user.mention}!')


@bot.tree.command(name="getplayer")
@app_commands.describe(bungie_id = "Your bungie id")
async def GetPlayer(interaction: discord.Interaction, bungie_id: str):

	memId = destiny.GetMembershipIdFromBungieId(bungie_id, 1)

	await interaction.response.send_message(f"{interaction.user.name}, your membership id is {memId}", ephemeral=True)


bot.run(DISCORD_API_TOKEN)