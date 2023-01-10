import discord
from discord import app_commands
from discord.ext import commands, tasks
import pickle
import PyDest
import pprint
from keys import BUNGIE_API_TOKEN

destiny = PyDest.PyDest(BUNGIE_API_TOKEN)

memId = 4611686018450187988  # My hardcoded membership Id
characterId = 2305843009379416333  # My hardcoded character Id
XUR_HASH = 2190858386 # Xur's vendor hash


class Weeklies(commands.Cog):
	def __init__(self, bot) -> None:
		self.client = bot


	@app_commands.command(name='pullnightfall', description='Get and save nightfall data')
	async def PullNightfall(self, interaction: discord.Interaction):

		filename = open('data/nightfall_data', 'wb')
		await interaction.response.send_message("Nighfall data dumped", ephemeral=True)


		character = destiny.api.get_character(1, memId, characterId, [204])

		# Cycle through and decode the activities
		for activity in character['Response']['activities']['data']['availableActivities']:
			decoded = destiny.decode_hash(activity['activityHash'], 'DestinyActivityDefinition')

			# Find the Master Nightfall activity and decode it
			if 'Nightfall: Master' in decoded['displayProperties']['name']:
				pickle.dump(decoded, filename)
				filename.close()

				# pprint.pprint(decoded)

				print("Nighfall data dumped")



	# TODO: Get Xur data and save into file
	@app_commands.command(name='pullxur', description='Get and save xur\'s current inventory')
	async def PullXur(self, interaction: discord.Interaction):

		final_dict = {}
		await interaction.response.send_message(content="Xur data dumped", ephemeral=True)

		# Serialize oauth data from file
		with open('data/oauth', 'rb') as filename:
			file_data = filename.read()

		# Load oauth data into dictionary
		oauth: dict = pickle.loads(file_data)
		access_token = oauth['access_token']

		print(access_token)

		# Get ADA-1 inventory
		xur = destiny.api.get_vendor(1, memId, characterId, XUR_HASH, access_token, [402])

		# pprint.pprint(xur)

		for itemIndex in xur['Response']['sales']['data']:
			item_hash = xur['Response']['sales']['data'][itemIndex]['itemHash']

			item = destiny.decode_hash(item_hash, 'DestinyInventoryItemDefinition')

			final_dict.update({item_hash: item})


		# Open file to save ADA-1 data
		filename = open('data/xur', 'wb')
		pickle.dump(final_dict, filename)
		filename.close()

		pprint.pprint(final_dict)

		print("Xur inventory dumped")


async def setup(bot):
	await bot.add_cog(Weeklies(bot))
