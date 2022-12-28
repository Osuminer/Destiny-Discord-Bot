import pydest
import discord
from discord import app_commands
from discord.ext import tasks, commands
import pprint
import asyncio

# Set api key values from file
with open('.env', 'r') as f:
	DISCORD_API_KEY = f.readline().rstrip('\n')
	BUNGIE_API_KEY = f.readline().rstrip('\n')

# Setup discord bot
bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())

# Setup pydest api wrapper
destiny = pydest.Pydest(BUNGIE_API_KEY)


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

# @tasks.loop(count=1)
async def SearchId(bungie_id: str):
	player_details = await destiny.api.search_destiny_player(1, bungie_id)
	memId = player_details['Response'][0]['membershipId']
	print(memId)
	return memId

memId = int()

@bot.tree.command(name="getplayer")
@app_commands.describe(bungie_id = "Your bungie id")
async def GetPlayer(interaction: discord.Interaction, bungie_id: str):
	bot.loop.create_task(SearchId(bungie_id))
	await interaction.response.send_message(f"{interaction.user.name}, your membership id is {memId}", ephemeral=True)


bot.run(DISCORD_API_KEY)