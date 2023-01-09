import discord
from discord import app_commands, ui
from discord.ext import commands, tasks
from requests_oauthlib import OAuth2Session
from keys import OAUTH_CLIENT_ID, OAUTH_SECRET
import pprint
import pickle


OAUTH_AUTH_URL = 'https://www.bungie.net/en/OAuth/Authorize'
REDIRECT_URL = 'https://osuminer.github.io/Projects/'
TOKEN_URL = 'https://www.bungie.net/platform/app/oauth/token/'

class Oauth(commands.Cog):
	def __init__(self, bot: discord.Client) -> None:
		self.bot = bot
		self.session = OAuth2Session(client_id=OAUTH_CLIENT_ID,
								redirect_uri=REDIRECT_URL)

	# Get oauth authorization code
	@app_commands.command(name='getauth', description='Get Bungie API authorization link and access token')
	async def GetAuth(self, interaction: discord.Interaction):

		auth_link = self.session.authorization_url(OAUTH_AUTH_URL)

		await interaction.response.send_message(f'Your authourization link in {auth_link[0]}\nPaste your code:', ephemeral=True)
		code = await self.bot.wait_for('message')
		print(code.content)

		await self.GetAccessToken(code.content)

	# Get oauth access token
	async def GetAccessToken(self, code):
		headers = {'Content-Type': 'application/x-www-form-urlencoded',
				   'Authorization': 'Basic NDIyMjE6MXZXckc0UXctcklwMlZwM1ZTc05YZUY1eFVRSHYtc1czMTNoR2FvaWtXaw=='}
		payload = {'grant_type': 'authorization_code',
				   'code': code}

		r = self.session.post(
			url=TOKEN_URL,
			headers=headers,
			data=payload
		).json()

		filename = open('data/oauth', 'wb')
		pickle.dump(r, filename)
		filename.close()

	# TODO: Refresh access token
	@app_commands.command(name='refreshtoken', description='Refresh Bungie API access token')
	async def RefreshToken(self, interaction: discord.Interaction):
		with open('data/oauth', 'rb') as filename:
			file_data = filename.read()

		oauth = pickle.loads(file_data)
		refresh_token = oauth['refresh_token']

		headers = {'Content-Type': 'application/x-www-form-urlencoded',
				   'Authorization': 'Basic NDIyMjE6MXZXckc0UXctcklwMlZwM1ZTc05YZUY1eFVRSHYtc1czMTNoR2FvaWtXaw=='}

		payload = {'grant_type': 'refresh_token',
				   'refresh_token': refresh_token}

		r = self.session.post(
			url=TOKEN_URL,
			headers=headers,
			data=payload
		).json()

		filename = open('data/oauth', 'wb')
		pickle.dump(r, filename)
		filename.close()

		await interaction.response.send_message("Access token was refreshed", ephemeral=True)

	# Possibly store everyone's oauth jsons in a database


async def setup(bot):
	await bot.add_cog(Oauth(bot))

# Modal for auth token input
class auth_response(ui.Modal, title="Auth Reponse"):
	code = ui.TextInput(label='Input Code', style=discord.TextStyle.short)

	async def on_submit(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(self.code)