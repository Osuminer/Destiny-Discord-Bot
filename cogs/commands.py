import discord
from discord import app_commands
from discord.ext import commands, tasks
import pickle
import PyDest
import pprint
from keys import BUNGIE_API_TOKEN

destiny = PyDest.PyDest(BUNGIE_API_TOKEN)

TOP_MODIFIERS = ['Shielded Foes', 'Champion Foes', 'Double Nightfall Drops', 'Ashes to Ashes', 'Lightning Crystals',
                 'Acute Arc Burn', 'Match Game', 'Champions: Mob', 'Attrition']



class Commands(commands.Cog):
	def __init__(self, bot) -> None:
		self.client = bot

	@app_commands.command(name="hello", description='Test command')
	async def hello(self, interaction: discord.Interaction):
		await interaction.response.send_message(f'Hey {interaction.user.mention}!')

	# Print Nightfall data
	@app_commands.command(name='nightfall', description='Pull data from the current master nightfall')
	async def Nightfall(self, interaction: discord.Interaction):

		# Serialize nightfall data from file
		with open('data/nightfall_data', 'rb') as filename:
			fileData = filename.read()

		# Load the saved dictionary file for the nightfall data
		nightfallData: dict = pickle.loads(fileData)

		name = nightfallData['displayProperties']['description']
		imageURL = destiny.api.get_image_url(nightfallData['pgcrImage'])
		thumbnailURL = destiny.api.get_image_url(nightfallData['displayProperties']['icon'])

		modifierList = list()
		modifierDesc = list()

		# Decode the modifiers
		for modifiers in nightfallData['modifiers']:
			modifierHash = modifiers['activityModifierHash']
			activityDecoded = destiny.decode_hash(
				modifierHash, 'DestinyActivityModifierDefinition')

			activityName = activityDecoded['displayProperties']['name']

			if (activityName in TOP_MODIFIERS) and (activityName not in modifierList):
				modifierList.append(activityDecoded['displayProperties']['name'])
				modifierDesc.append(activityDecoded['displayProperties']['description'])

		for i in range(len(modifierList)):
			modifierList[i] = '- ' + modifierList[i]

		embed = discord.Embed(title=name, color=0x1f8b4c)
		embed.set_author(name="Nightfall: Master")
		embed.set_image(url=imageURL)
		embed.set_thumbnail(url=thumbnailURL)
		embed.add_field(name="Modifiers", value='\n'.join(modifierList))
		pprint.pprint(modifierList)
		# for i in range(len(modifierList)):
		# 	embed.add_field(name=modifierList[i], value=modifierDesc[i])

		await interaction.response.send_message(embed=embed)

	# Pull ADA-1's current inventory
	@app_commands.command(name='ada-1', description='Pull ADA-1\'s current inventory')
	async def ADA1(self, interaction: discord.Interaction):

		mods = list()

		# Serialize ADA-1 data from file
		with open('data/ada1', 'rb') as filename:
			file_data = filename.read()

		# Load data from read bytes
		ada: dict = pickle.loads(file_data)

		# Make a list of only the mods she is selling
		for val in ada.values():
			name = val['displayProperties']['name']
			item_type = val['itemType']

			if item_type == 19:
				mods.append("- " + name)

		image_url = destiny.api.get_image_url('/common/destiny2_content/icons/fc945fd08122485639db8778052ce498.png')

		embed = discord.Embed(title='ADA-1')
		embed.set_thumbnail(url=image_url)
		embed.add_field(name="Mods", value='\n'.join(mods))

		await interaction.response.send_message(embed=embed)
		

async def setup(bot):
	await bot.add_cog(Commands(bot))