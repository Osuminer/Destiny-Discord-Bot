import pydest
import discord

with open('.env', 'r') as f:
	DISCORD_API_KEY = f.readline().rstrip('\n')
	BUNGIE_API_KEY = f.readline().rstrip('\n')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} has connected')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith("$test"):
		print('test')
		await message.channel.send("test")


client.run(DISCORD_API_KEY)