import requests
import urllib

from PyDest.api import API
from PyDest.manifest import Manifest


class PyDest:
    def __init__(self, apiKey):
        self._apiKey = apiKey
        self.api = API(self._apiKey)
        self._manifest = Manifest(PyDest)

    def decode_hash(self, hash_id, definition, language="en"):
        """Get the corresponding static info for an item given it's hash value from the Manifest

        Args:
            hash_id:
                The unique identifier of the entity to decode
            definition:
                The type of entity to be decoded (ex. 'DestinyClassDefinition')
            lanauge:
                The language to use when retrieving results from the Manifest

        Returns:
            dict: json corresponding to the given hash_id and definition

        Raises:
            PydestException
        """
        return self._manifest.decode_hash(hash_id, definition, language)

    async def update_manifest(self, language='en'):
        """Update the manifest if there is a newer version available

        Args:
            language [optional]:
                The language corresponding to the manifest to update
        """
        await self._manifest.update_manifest(language)


class PydestException(Exception):
    pass
