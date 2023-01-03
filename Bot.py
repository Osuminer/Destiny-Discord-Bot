from keys import DISCORD_API_TOKEN, BUNGIE_API_TOKEN
import PyDest
import discord
from discord import app_commands
from discord.ext import tasks, commands
import pprint

# Setup discord bot
bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())

# Setup pydest api wrapper
destiny = PyDest.PyDest(BUNGIE_API_TOKEN)
HEADERS = {"X-API-Key":BUNGIE_API_TOKEN}

# Sync commands with Discord on bot startup
@bot.event
async def on_ready():
	print(f'{bot.user} has connected')

	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} commands\n")
	except Exception as e:
		print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
	await interaction.response.send_message(f'Hey {interaction.user.mention}!')


@bot.tree.command(name="getmemid")
@app_commands.describe(bungie_id = "Enter your bungie id")
async def GetPlayer(interaction: discord.Interaction, bungie_id: str):

	player = destiny.api.search_destiny_player(1, bungie_id)
	memId = player['Response'][0]['membershipId']

	print(f"{interaction.user.name}, your membership id is {memId}")
	await interaction.response.send_message(f"{interaction.user.name}, your membership id is {memId}", ephemeral=True)

@bot.tree.command(name="nightfall")
async def Nightfall(interaction: discord.Interaction):
	memId = 4611686018430110693
	characterId = 2305843009265615844
	character = destiny.api.get_character(1, memId, characterId, [204])

	for activity in character['Response']['activities']['data']['availableActivities']:
		decoded = destiny.decode_hash(activity['activityHash'], 'DestinyActivityDefinition')

		if 'Nightfall: Master' in decoded['displayProperties']['name']:
			name = decoded['displayProperties']['description']

			modifierList = list()

			for modifiers in decoded['modifiers']:
				modifierHash = modifiers['activityModifierHash']
				y = destiny.decode_hash(modifierHash, 'DestinyActivityModifierDefinition')
				# print(y['displayProperties']['name'])
				# print(y['displayProperties']['description'])
				modifierList.append(y['displayProperties']['name'])

	retVal = ','.join(modifierList)

	await interaction.response.send_message(retVal)

bot.run(DISCORD_API_TOKEN)