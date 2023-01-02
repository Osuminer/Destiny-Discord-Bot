import requests

DESTINY2_URL = 'https://www.bungie.net/Platform/Destiny2/'
USER_URL = 'https://www.bungie.net/Platform/User/'
GROUP_URL = 'https://www.bungie.net/Platform/GroupV2/'

class PyDest:
	def __init__(self, apiKey):
		self.apiKey = apiKey
		self.HEADERS = {"X-API-Key":self.apiKey}

	def SearchDestinyPlayer(self, displayName, membershipType=-1):
		displayName = displayName.replace('#', '%23')

		url = DESTINY2_URL + "SearchDestinyPlayer/{}/{}/"
		url = url.format(membershipType, displayName)

		return requests.get(url, headers=self.HEADERS).json()

	def GetMembershipIdFromBungieId(self, displayName, membershipType=-1):
		displayName = displayName.replace('#', '%23')

		url = DESTINY2_URL + "SearchDestinyPlayer/{}/{}/"
		url = url.format(membershipType, displayName)

		return requests.get(url, headers=self.HEADERS).json()['Response'][0]['membershipId']

	def GetProfileInfo(self, membershipId, membershipType, components):
		url = DESTINY2_URL + "{}/Profile/{}/?components={}"
		url = url.format(membershipType, membershipId, components)

		return requests.get(url, headers=self.HEADERS).json()
