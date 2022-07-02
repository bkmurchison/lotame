from lotame.api import Api


class BehaviorService(object):
    """
    # BehaviorService Class
    #   Provides helper methods for the Lotame API behavior service
    """
    # statics
    BEHAVIOR_SERVICE = "/behaviors"

    def __init__(self, api=None):
        if api is None:
            api = Api()
        self.api = api

    def get(self, behavior=""):
        url = self.api.build_url(
            self.BEHAVIOR_SERVICE + "/" + str(behavior), {}, False)
        behavior = self.api.get(url)
        return behavior

    def getList(self, params={}):
        url = self.api.build_url(self.BEHAVIOR_SERVICE, params)
        behavior_list = self.api.get(url)
        return behavior_list
