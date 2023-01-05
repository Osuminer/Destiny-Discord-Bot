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
bot = commands.Bot(command_prefix=".", intents=discord.Intents.default())

# Setup pydest api wrapper
destiny = PyDest.PyDest(BUNGIE_API_TOKEN)
HEADERS = {"X-API-Key": BUNGIE_API_TOKEN}

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


# Print Nightfall information
@bot.tree.command(name="nightfall")
async def Nightfall(interaction: discord.Interaction):
    memId = 4611686018430110693  # My hardcoded membership Id
    characterId = 2305843009265615844  # My hardcoded character Id

    character = destiny.api.get_character(1, memId, characterId, [204])

    # Cycle through and decode the activities
    for activity in character['Response']['activities']['data']['availableActivities']:
        decoded = destiny.decode_hash(
            activity['activityHash'], 'DestinyActivityDefinition')

        # Find the Master Nightfall activity and decode it
        if 'Nightfall: Master' in decoded['displayProperties']['name']:
            name = decoded['displayProperties']['description']
            imageURL = destiny.api.get_image_url(decoded['pgcrImage'])
            thumbnailURL = destiny.api.get_image_url(
                decoded['displayProperties']['icon'])
            # description = decoded['selectionScreenDisplayProperties']['description']

            modifierList = list()
            modifierDesc = list()

            # Decode the modifiers
            for modifiers in decoded['modifiers']:
                modifierHash = modifiers['activityModifierHash']
                activityDecoded = destiny.decode_hash(
                    modifierHash, 'DestinyActivityModifierDefinition')

                activityName = activityDecoded['displayProperties']['name']

                # if (activityName in TOP_MODIFIERS) and (activityName not in modifierList):
                if (activityName in TOP_MODIFIERS):
                    modifierList.append(
                        activityDecoded['displayProperties']['name'])
                    modifierDesc.append(
                        activityDecoded['displayProperties']['description'])

    embed = discord.Embed(title=name, color=0x1f8b4c)
    embed.set_author(name="Nightfall: Master")
    embed.set_image(url=imageURL)
    embed.set_thumbnail(url=thumbnailURL)
    # embed.add_field(name="Modifiers", value=', '.join(modifierList))
    for i in range(len(modifierList)):
        embed.add_field(name=modifierList[i], value=modifierDesc[i])

    await interaction.response.send_message(embed=embed)

bot.run(DISCORD_API_TOKEN)
