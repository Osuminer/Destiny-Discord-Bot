import discord
from discord import app_commands
from discord.ext import commands, tasks
from keys import BUNGIE_API_TOKEN
import PyDest
import pprint
import pickle

destiny = PyDest.PyDest(BUNGIE_API_TOKEN)

memId = 4611686018450187988  # My hardcoded membership Id
characterId = 2305843009379416333  # My hardcoded character Id
ADA_HASH = 350061650 # Ada-1 vendor hash

class Dailies(commands.Cog):
	def __init__(self, bot) -> None:
		self.client = bot

	# Get ADA-1 data and save into file
	@app_commands.command(name='pullada-1', description='Get and save ADA-1\'s current inventory')
	async def PullADA1(self, interaction: discord.Interaction):

		final_dict = {}
		await interaction.response.send_message(content="ADA-1 data dumped", ephemeral=True)

		# Serialize oauth data from file
		with open('data/oauth', 'rb') as filename:
			file_data = filename.read()

		# Load oauth data into dictionary
		oauth = pickle.loads(file_data)
		access_token = oauth['access_token']

		# Get ADA-1 inventory
		ada = destiny.api.get_vendor(1, memId, characterId, ADA_HASH, access_token, [400,402])

		# pprint.pprint(ada)

		for itemIndex in ada['Response']['sales']['data']:
			item_hash = ada['Response']['sales']['data'][itemIndex]['itemHash']

			item = destiny.decode_hash(item_hash, 'DestinyInventoryItemDefinition')

			final_dict.update({item_hash: item})


		# Open file to save ADA-1 data
		filename = open('data/ada1', 'wb')
		pickle.dump(final_dict, filename)
		filename.close()

		print("ADA-1 inventory dumped")


	# TODO: Get Gunsmith data and save into file

async def setup(bot):
	await bot.add_cog(Dailies(bot))
