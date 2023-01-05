import discord
from discord import app_commands
from discord.ext import commands, tasks

class Dailies(commands.Cog):
	def __init__(self, bot) -> None:
		self.client = bot


async def setup(bot):
	await bot.add_cog(Dailies(bot))
