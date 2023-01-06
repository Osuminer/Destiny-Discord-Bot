import discord
from discord import app_commands
from discord.ext import commands, tasks

class Oauth(commands.Cog):
	def __init__(self, bot) -> None:
		self.client = bot

	# TODO: Get oauth authorization code

	# TODO: Get oauth access token

	# TODO: Get oauth refresh token

	# TODO: Refresh access token

	# TODO: Serialize into dictionary


async def setup(bot):
	await bot.add_cog(Oauth(bot))