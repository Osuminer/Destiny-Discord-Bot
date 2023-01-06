import discord
from discord import app_commands
from discord.ext import commands, tasks

class Weeklies(commands.Cog):
	def __init__(self, bot) -> None:
		self.client = bot

	# TODO: Get nightfall data and save into file
	
	# TODO: Get Xur data and save into file

async def setup(bot):
	await bot.add_cog(Weeklies(bot))