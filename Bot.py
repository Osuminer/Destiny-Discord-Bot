import pydest
import discord
from discord import app_commands
from discord.ext import commands


with open('.env', 'r') as f:
	DISCORD_API_KEY = f.readline().rstrip('\n')
	BUNGIE_API_KEY = f.readline().rstrip('\n')

bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())


@bot.event
async def on_ready():
	print(f'{bot.user} has connected')
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} commands")
	except Exception as e:
		print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
	await interaction.response.send_message(f'Hey {interaction.user.mention}!')



bot.run(DISCORD_API_KEY)