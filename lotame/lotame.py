"""
Python Lotame API wrapper.
==========================
Filename: lotame.py
Author: Paulo Kuong
Email: pkuong80@gmail.com
Python Version: 3.6.1+

Please refer to https://api.lotame.com/docs/#/ to get all Endpoints.
Please refer to README for examples.
"""
import json
from datetime import datetime, timedelta

import requests


class Credentials(object):
    DEFAULT_BASE_URL = 'https://api.lotame.com/2'

    def __init__(self, client_id=None, token=None, access=None, base_url=None):

        if not client_id or not token or not access:
            raise Exception(
                "Missing credentials. All client_id, token and access are "
                "required.")
        self.client_id = client_id
        self.token = token
        self.access = access
        self.base_url = base_url or Credentials.DEFAULT_BASE_URL


class Api(object):
    """
    # Api Class
    #   Imports credentials using Credentials Class
    #   Utilizes stored credentials to authenticate requests to Lotame Api
    #   Provides helper methods for service authentication and api actions
    """
    # static class variables
    REQUEST_GET = "REQUEST_GET"
    REQUEST_POSTBODY = "REQUEST_POSTBODY"
    REQUEST_POST = "REQUEST_POST"
    REQUEST_PUT = "REQUEST_PUT"
    REQUEST_DELETE = "REQUEST_DELETE"
    DEFAULT_PYTHON_HEADER = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
        "User-Agent": "python"
    }
    DEFAULT_JSON_RECEIVE_HEADER = {'Accept': 'application/json'}
    DEFAULT_JSON_SEND_HEADER = {
        'Content-type': 'application/json', 'Accept': 'application/json'}

    # initialization method
    # allows specification of custom properties file and profile
    # allows passing authentication parameters directly in lieu of properties file
    def __init__(self, credentials=None):
        if credentials is None:
            credentials = Credentials()
        self.credentials = credentials

    # TODO: this needs to be made 'private' and invoked with _perform_request
    def buildUrl(self, service="", params={}, auto_assign_client_id=True):
        if service == "":
            return ""
        url = self.credentials.base_url + service
        if auto_assign_client_id is True:
            url = url + "?client_id=" + str(self.credentials.client_id)
        for key, val in params.items():
            if isinstance(val, list):
                for v in val:
                    url = self._populate_url_params(url, key, v)
            else:
                url = self._populate_url_params(url, key, val)
        return url

    @staticmethod
    def _populate_url_params(url="", key="", val=""):
        if "?" not in url:
            url = url + "?" + str(key) + "=" + str(val)
        else:
            url = url + "&" + str(key) + "=" + str(val)
        return url

    def _merge_headers(self, base_headers):
        headers = {}
        headers.update(base_headers)
        auth_headers = {
            'x-lotame-token': self.credentials.token,
            'x-lotame-access': self.credentials.access
        }
        headers.update(auth_headers)
        return headers

    def _perform_request(
            self, service="", user=None, access=None, type=None, headers=None,
            body=None):
        full_headers = self._merge_headers(headers)
        if type == self.REQUEST_GET:
            response = requests.get(service, headers=full_headers)
        elif type == self.REQUEST_POSTBODY:
            response = requests.post(
                service, data=json.dumps(body), headers=full_headers)
        elif type == self.REQUEST_POST:
            response = requests.post(service, headers=full_headers)
        elif type == self.REQUEST_PUT:
            response = requests.put(
                service, data=json.dumps(body), headers=full_headers)
        elif type == self.REQUEST_DELETE:
            response = requests.delete(service, headers=full_headers)
        else:  # TODO: this should no longer happen, probably preferable to raise an exception
            response = "Invalid request type"
        return response

    def get(self, service, user=None, access=None):
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_GET,
            headers=self.DEFAULT_JSON_RECEIVE_HEADER
        ).json()

    def postBody(self, service="", body="", user=None, access=None):
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_POSTBODY,
            headers=self.DEFAULT_JSON_SEND_HEADER,
            body=body
        ).json()

    def post(self, service="", user=None, access=None):
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_POST,
            headers=self.DEFAULT_JSON_SEND_HEADER
        ).json()

    def put(self, service="", body="", user=None, access=None):
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_PUT,
            headers=self.DEFAULT_JSON_SEND_HEADER,
            body=body
        ).json()

    def delete(self, service="", user=None, access=None):
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_DELETE,
            headers=self.DEFAULT_JSON_RECEIVE_HEADER
        ).json()


class FirehoseService(object):
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

    def __init__(self, api=None):
        if api is None:
            api = Api()
        self.api = api

    def getFeeds(self, params={}):
        url = self.api.buildUrl(self.FIREHOSE_FEEDS, params)
        feeds_response = self.api.get(url)
        feeds = []
        for feed_json in feeds_response['feeds']:
            feeds.append(feed_json)
        return feeds

    def getUpdatesForFeed(self, feed_id=0, params={}):
        if params == {}:
            params = {self.FEED_ID: feed_id}
        else:
            params[self.FEED_ID] = feed_id
        url = self.api.buildUrl(self.FIREHOSE_UPDATES, params)
        feed_updates_response = self.api.get(url)
        return feed_updates_response

    def getUpdatesForFeeds(self, feeds=[], params={}):
        feeds_updates_responses = []
        for feed in feeds:
            feeds_updates_responses.append(
                self.getUpdatesForFeed(feed['id'], params))
        return feeds_updates_responses

    def getUpdates(self, hours=DEFAULT_HOURS, minutes=DEFAULT_MINUTES, since=DEFAULT_UTC):
        params = {}
        if since:
            since_utc = str(int(round(since)))
        elif hours or minutes:
            since_utc = str(int(round(
                ((datetime.utcnow() - timedelta(
                    hours=hours, minutes=minutes)) - datetime(1970, 1, 1)).total_seconds())))
            params = {"since": since_utc}
        feeds = self.getFeeds()
        updates = self.getUpdatesForFeeds(feeds, params)
        return updates


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
        url = self.api.buildUrl(
            self.BEHAVIOR_SERVICE + "/" + str(behavior), {}, False)
        behavior = self.api.get(url)
        return behavior

    def getList(self, params={}):
        url = self.api.buildUrl(self.BEHAVIOR_SERVICE, params)
        behavior_list = self.api.get(url)
        return behavior_list


class AudienceService(object):
    """
    # AudienceService Class
    #   Provides helper methods for the Lotame API audience service
    """
    # statics
    AUDIENCE_SERVICE = "/audiences"

    def __init__(self, api=None):
        if api is None:
            api = Api()
        self.api = api

    def get(self, audience=""):
        url = self.api.buildUrl(
            self.AUDIENCE_SERVICE + "/" + str(audience), {}, False)
        audience = self.api.get(url)
        return audience

    def getList(self, params={}):
        url = self.api.buildUrl(self.AUDIENCE_SERVICE, params)
        audience_list = self.api.get(url)
        return audience_list

    def get_create_audience_json(
            self, audience_name, client_id, behavior_groups, description='',
            condition_between_grouops='OR', condition_within_group='AND',
            **custom_request_params):
        """Constructs minimal json audience definition.

        behavior_groups (list): list of behavior ids.
            For example: [[244, 343, 345], [33, 235]]
            Where there is AND condition between ids in the sub list, and
            OR condition on the groups of sub lists, that is:
            [[244 AND 343 AND 345] OR [33 AND 235]]

        Args:
            audience_name (str): audience name.
            client_id (int): id of client this audience should belong to.
            behavior_groups (list): 2 dimensional list of behavior ids.
            description (str[optional]): description of this audience.
            condition_between_grouops (str[optional]): condition between groups of behaviors.
            condition_within_group (str[optional]): condition within each group of behaviors.
            custom_request_params (dict): custom request params.
        Returns:
            dict: audience definition:
                {
                  'name': audience_name,
                  'clientId': client_id,
                  'definition': ....,
                  'description': '.......'
                }
        """
        component = []
        for index, behavior_group in enumerate(behavior_groups):
            tmp = {
                'operator': None
            }
            if len(behavior_group) == 1:
                tmp['complexAudienceBehavior'] = {
                    'purchased': True,
                    'behavior': {
                        'id': behavior_group[0]
                    },
                }
            else:
                tmp['component'] = []
                for index2, behavior in enumerate(behavior_group):
                    tmp2 = {
                        'operator': None,
                        'complexAudienceBehavior': {
                            'purchased': True,
                            'behavior': {
                                'id': behavior
                            }
                        }
                    }
                    if index2 != 0:
                        tmp2['operator'] = condition_within_group
                    tmp['component'].append(tmp2)
            if index != 0:
                tmp['operator'] = condition_between_grouops
            component.append(tmp)

        definition = {
            'name': audience_name,
            'clientId': client_id,
            'definition': {'component': component}
        }
        if len(custom_request_params.items()) > 0:
            for k, v in custom_request_params.items():
                if k not in ['name', 'clientId', 'definition']:
                    definition[k] = v
        if 'overlap' not in definition:
            definition['overlap'] = True

        if description:
            definition['description'] = description
        return definition
