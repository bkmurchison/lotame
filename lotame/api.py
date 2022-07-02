import json
from typing import Dict, Any

import requests

from lotame.credentials import Credentials


class Api:
    """
    # Api Class
    #   Imports credentials using Credentials Class
    #   Utilizes stored credentials to authenticate requests to Lotame Api
    #   Provides helper methods for service authentication and api actions
    """
    # static class variables
    REQUEST_GET = "REQUEST_GET"
    REQUEST_POST_BODY = "REQUEST_POST_BODY"
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
    def __init__(self, credentials: Credentials = None):
        if credentials is None:
            raise Exception("Missing credentials.  Credentials instance is required.")
        self.credentials = credentials

    def get(self,
            service: str,
            user: str = None,
            access: str = None) -> Dict[str, Any]:
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            request_type=self.REQUEST_GET,
            headers=self.DEFAULT_JSON_RECEIVE_HEADER
        ).json()

    def post_body(self,
                  service: str = "",
                  body: str = "",
                  user: str = None,
                  access: str = None) -> Dict[str, Any]:
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            request_type=self.REQUEST_POST_BODY,
            headers=self.DEFAULT_JSON_SEND_HEADER,
            body=body
        ).json()

    def post(self,
             service: str = "",
             user: str = None,
             access: str = None) -> Dict[str, Any]:
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            request_type=self.REQUEST_POST,
            headers=self.DEFAULT_JSON_SEND_HEADER
        ).json()

    def put(self,
            service: str = "",
            body: str = "",
            user: str = None,
            access: str = None) -> Dict[str, Any]:
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            request_type=self.REQUEST_PUT,
            headers=self.DEFAULT_JSON_SEND_HEADER,
            body=body
        ).json()

    def delete(self,
               service: str = "",
               user: str = None,
               access: str = None):
        return self._perform_request(
            service=service,
            user=user,
            access=access,
            request_type=self.REQUEST_DELETE,
            headers=self.DEFAULT_JSON_RECEIVE_HEADER
        ).json()

    def _perform_request(self,
                         service: str = "",
                         user: str = None,
                         access: str = None,
                         request_type: str = None,
                         headers: Dict[str, str] = None,
                         body: str = None):
        full_headers = self._merge_headers(headers)
        if request_type == self.REQUEST_GET:
            response = requests.get(service, headers=full_headers)
        elif request_type == self.REQUEST_POST_BODY:
            response = requests.post(service, data=json.dumps(body), headers=full_headers)
        elif request_type == self.REQUEST_POST:
            response = requests.post(service, headers=full_headers)
        elif request_type == self.REQUEST_PUT:
            response = requests.put(service, data=json.dumps(body), headers=full_headers)
        elif request_type == self.REQUEST_DELETE:
            response = requests.delete(service, headers=full_headers)
        else:  # TODO: this should no longer happen, probably preferable to raise an exception
            response = "Invalid request type"
        return response

    def _merge_headers(self, base_headers):
        headers = {}
        headers.update(base_headers)
        auth_headers = {
            'x-lotame-token': self.credentials.token,
            'x-lotame-access': self.credentials.access
        }
        headers.update(auth_headers)
        return headers
