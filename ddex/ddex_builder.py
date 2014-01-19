from DDEXUI.ddex.ddex import DDEX
from DDEXUI.ddex.resource import Resource
from DDEXUI.ddex.release import ReleaseIdType

class DDEXBuilder:
    def __init__(self):
        self._resources = []
        self._releases = []
        self._sender = None
        self._recipient = None
        self._is_update = None

    def recipient(self, recipient):
        self._recipient = recipient
        return self
    
    def sender(self, sender) :
        self._sender = sender
        return self

    def add_release(self, release):
        self._releases.append(release)
        return self

    def add_product_release(self, release):
        self._releases.insert(0, release)
        return self

    def add_resource(self, resource):
        self._resources.append(resource)
        return self

    def update(self, is_update):
        self._is_update = is_update
        return self

    def build(self):
        return DDEX(self._sender, self._recipient, self._releases, self._resources, self._is_update)

    def get_upc(self):
        try:
             return list(filter(lambda release: release.release_id.type == ReleaseIdType.Upc, self._releases))[0].release_id.id
        except Exception as e:
            print("No product release!")
            raise e
