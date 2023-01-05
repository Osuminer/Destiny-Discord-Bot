import discord
from discord import app_commands
from discord.ext import commands, tasks

class Commands(commands.Cog):
	def __init__(self, bot) -> None:
		self.client = bot

	@app_commands.command(name='test')
	async def Test(self, interaction: discord.Interaction):
		await interaction.response.send_message("test")

	@app_commands.command(name="hello")
	async def hello(interaction: discord.Interaction):
		await interaction.response.send_message(f'Hey {interaction.user.mention}!')


async def setup(bot):
	await bot.add_cog(Commands(bot))