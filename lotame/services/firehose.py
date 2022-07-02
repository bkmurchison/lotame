from datetime import timedelta, datetime
from typing import Dict, Any, List

from lotame import utils
from lotame.api import Api


class FirehoseService:
    """
    # FirehoseService Class
    #   Provides helper methods for the Lotame API firehose service
    """
    # statics
    FIREHOSE_FEEDS = "/firehose/feeds"
    FIREHOSE_UPDATES = "/firehose/updates"
    DEFAULT_HOURS = 24
    DEFAULT_MINUTES = 0
    DEFAULT_UTC = 0
    FEED_ID = "feed_id"

    def __init__(self, api: Api = None):
        if api is None:
            api = Api()
        self.api = api

    def get_feeds(self, params: Dict[Any, Any] = {}):
        url = self.api.build_url(self.FIREHOSE_FEEDS, params)
        feeds_response = self.api.get(url)
        return [feed_json for feed_json in feeds_response['feeds']]

    def get_updates_for_feed(self,
                             feed_id: int = 0,
                             params: Dict[Any, Any] = {}):
        if params is None or not isinstance(params, dict):
            params = {}

        params[self.FEED_ID] = feed_id
        url = utils.build_url(self.api.credentials, self.FIREHOSE_UPDATES, params)
        feed_updates_response = self.api.get(url)
        return feed_updates_response

    def get_updates_for_feeds(self,
                              feeds: List[Dict[str, Any]] = [],
                              params: Dict[Any, Any] = {}):
        return [self.get_updates_for_feed(feed['id'], params) for feed in feeds]

    def get_updates(self, hours=DEFAULT_HOURS, minutes=DEFAULT_MINUTES, since=DEFAULT_UTC):
        params = {}
        if since:
            since_utc = str(int(round(since)))
        elif hours or minutes:
            since_utc = str(int(round(
                ((datetime.utcnow() - timedelta(
                    hours=hours, minutes=minutes)) - datetime(1970, 1, 1)).total_seconds())))
        if since_utc:
            params["since"] = since_utc

        feeds = self.get_feeds()
        updates = self.get_updates_for_feeds(feeds, params)
        return updates
