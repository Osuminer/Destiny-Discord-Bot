import discord
from discord import app_commands, ui
from discord.ext import commands, tasks
from requests_oauthlib import OAuth2Session
from keys import BUNGIE_API_TOKEN, OAUTH_CLIENT_ID
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

	# TODO: Get oauth authorization code
	@app_commands.command(name='getauth')
	async def GetAuth(self, interaction: discord.Interaction):

		auth_link = self.session.authorization_url(OAUTH_AUTH_URL)

		await interaction.response.send_message(f'Your authourization link in {auth_link[0]}\nPaste your code:', ephemeral=True)
		code = await self.bot.wait_for('message')
		print(code.content)

		await self.GetAccessToken(code.content)

		# await interaction.response.send_modal(auth_response())


	# TODO: Get oauth access token
	async def GetAccessToken(self, code):
		content_type = {'Content-Type': 'application/x-www-form-urlencoded'}
		payload = {'grant_type': 'authorization_code',
				'code': code,
				'client_id': OAUTH_CLIENT_ID}

		r = self.session.post(
			url=TOKEN_URL,
			headers=content_type,
			data=payload
		).json()

		filename = open('data/oauth', 'wb')
		pickle.dump(r, filename)
		filename.close()

		pprint.pprint(r)

	# TODO: Get oauth refresh token

	# TODO: Refresh access token

	# TODO: Serialize into dictionary

	# Possibly store everyone's oauth jsons in a database


async def setup(bot):
	await bot.add_cog(Oauth(bot))

class auth_response(ui.Modal, title="Auth Reponse"):
	code = ui.TextInput(label='Input Code', style=discord.TextStyle.short)

	async def on_submit(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message(self.code)