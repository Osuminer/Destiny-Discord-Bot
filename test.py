from requests_oauthlib import OAuth2Session
from keys import BUNGIE_API_TOKEN, OAUTH_CLIENT_ID
import pprint
import pickle

OAUTH_AUTH_URL = 'https://www.bungie.net/en/OAuth/Authorize'
REDIRECT_URL = 'https://osuminer.github.io/Projects/'
TOKEN_URL = 'https://www.bungie.net/platform/app/oauth/token/'
test = 'https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/'

session = OAuth2Session(client_id=OAUTH_CLIENT_ID, redirect_uri=REDIRECT_URL)

auth_link = session.authorization_url(OAUTH_AUTH_URL)

print(f'Auth link: {auth_link[0]}')

code = input("Paste your code: ")

content_type = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {'grant_type': 'authorization_code',
           'code': code,
           'client_id': OAUTH_CLIENT_ID}

r = session.post(
    url=TOKEN_URL,
    headers=content_type,
    data=payload
).json()

filename = open('data/oauth', 'wb')
pickle.dump(r, filename)
filename.close()

pprint.pprint(r)
token = r['access_token']

additional_headers = {'X-API-KEY': BUNGIE_API_TOKEN,
					  'authorization': 'Bearer ' + token}

r = session.get(url=test, headers=additional_headers).json()

pprint.pprint(r)
