import urllib
import requests

DESTINY2_URL = 'https://www.bungie.net/Platform/Destiny2/'
USER_URL = 'https://www.bungie.net/Platform/User/'
GROUP_URL = 'https://www.bungie.net/Platform/GroupV2/'


class API:
    def __init__(self, apiKey):
        self._apiKey = apiKey

    def _get_request(self, url):
        headers = {"X-API-Key": self._apiKey}
        encodedUrl = urllib.parse.quote(url, safe=':/?&=,.')

        try:
            retVal = requests.get(encodedUrl, headers=headers)
        except:
            raise "Could not connect to Bungie.net"

        return retVal.json()

    def SearchDestinyPlayer(self, displayName, membershipType=-1):
        url = DESTINY2_URL + "SearchDestinyPlayer/{}/{}/"
        url = url.format(membershipType, displayName)

        return self._get_request(url)

    def GetMembershipIdFromBungieId(self, displayName, membershipType=-1):
        url = DESTINY2_URL + "SearchDestinyPlayer/{}/{}/"
        url = url.format(membershipType, displayName)

        return self._get_request(url)['Response'][0]['membershipId']

    def GetProfileInfo(self, membershipId, membershipType, components):
        url = DESTINY2_URL + "{}/Profile/{}/?components={}"
        url = url.format(membershipType, membershipId, components)

        return self._get_request(url)

    def get_character(self, membership_type, membership_id, character_id, components):
        """Returns character information for the supplied character

        Args:
                membership_type (int):
                        A valid non-BungieNet membership type (BungieMembershipType)
                membership_id (int):
                        Destiny membership ID
                character_id (int):
                        ID of the character
                components (list):
                        A list containing the components  to include in the response.
                        (see Destiny.Responses.DestinyProfileResponse). At least one
                        component is required to receive results. Can use either ints
                        or strings.

        Returns:
                json (dict)
        """
        url = DESTINY2_URL + '{}/Profile/{}/Character/{}/?components={}'
        url = url.format(membership_type, membership_id,
                         character_id, ','.join([str(i) for i in components]))

        return self._get_request(url)
