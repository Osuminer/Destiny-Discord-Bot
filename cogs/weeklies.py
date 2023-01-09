import discord
from discord import app_commands
from discord.ext import commands, tasks
import pickle
import PyDest
from keys import BUNGIE_API_TOKEN

destiny = PyDest.PyDest(BUNGIE_API_TOKEN)


class Weeklies(commands.Cog):
	def __init__(self, bot) -> None:
		self.client = bot


	@app_commands.command(name='pullnightfall', description='Get and save nightfall data')
	async def PullNightfall(self, interaction: discord.Interaction):

		filename = open('data/nightfall_data', 'wb')
		await interaction.response.send_message("Nighfall data dumped")

		memId = 4611686018430110693  # My hardcoded membership Id
		characterId = 2305843009265615844  # My hardcoded character Id

		character = destiny.api.get_character(1, memId, characterId, [204])

		# Cycle through and decode the activities
		for activity in character['Response']['activities']['data']['availableActivities']:
			decoded = destiny.decode_hash(activity['activityHash'], 'DestinyActivityDefinition')

			# Find the Master Nightfall activity and decode it
			if 'Nightfall: Master' in decoded['displayProperties']['name']:
				pickle.dump(decoded, filename)
				filename.close()

				print("Nighfall data dumped")



	# TODO: Get Xur data and save into file
	@app_commands.command(name='pullxur', description='Get and save xur data')
	async def PullXur(self, interaction: discord.Interaction):
		pass


async def setup(bot):
	await bot.add_cog(Weeklies(bot))
