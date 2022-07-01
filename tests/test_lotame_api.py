import uuid
from typing import Dict, Any
from unittest.mock import patch, Mock

import pytest

from lotame.lotame import Credentials, Api


def create_resp(status_code: int, json_resp: Dict[str, Any]) -> Mock:
    m = Mock()
    m.status_code = status_code
    m.json.return_value = json_resp
    return m


@pytest.fixture()
def client_id() -> str:
    return "2967"


@pytest.fixture()
def token() -> str:
    return str(uuid.uuid4()).replace("-", "")


@pytest.fixture()
def access(token) -> str:
    return token[::-1]


@pytest.fixture()
def base_url() -> str:
    return "https://this/should/not/work"


@pytest.fixture()
def credentials(client_id, token, access, base_url) -> Credentials:
    return Credentials(client_id=client_id,
                       token=token,
                       access=access,
                       base_url=base_url)


def test_init_api_credentials_not_assigned():
    with pytest.raises(Exception) as e:
        Api()
    assert str(e.value) == "Missing credentials. All client_id, token and access are required."


def test_init_api_credentials_assigned(credentials):
    api = Api(credentials)
    assert api.credentials == credentials


@pytest.fixture
def service() -> str:
    return "service/to/invoke"


@pytest.fixture
def resp_json() -> Dict[str, Any]:
    return {}


@pytest.fixture
def get_resp_ok(resp_json) -> Mock:
    return create_resp(status_code=200, json_resp=resp_json)


@patch('lotame.lotame.requests')
def test_get_ok(mock_requests, credentials, service, get_resp_ok, resp_json):
    mock_requests.get.return_value = get_resp_ok
    api = Api(credentials)
    rsp = api.get(service=service)
    assert rsp == resp_json


@pytest.fixture
def post_body_req_json() -> Dict[str, Any]:
    return {'data1': 5, 'data2': 'Five', 'data3': 5.0}


@pytest.fixture
def post_body_resp_json(post_body_req_json) -> Dict[str, Any]:
    return post_body_req_json


@pytest.fixture
def post_body_resp_ok(post_body_resp_json) -> Mock:
    return create_resp(200, post_body_resp_json)


@patch('lotame.lotame.requests')
def test_post_body_ok(mock_requests,
                      credentials,
                      service,
                      post_body_resp_ok,
                      post_body_req_json,
                      post_body_resp_json):
    mock_requests.post.return_value = post_body_resp_ok

    api = Api(credentials=credentials)
    rsp = api.postBody(service=service, body=post_body_req_json)
    assert rsp == post_body_resp_json


@pytest.fixture
def post_resp_json(resp_json) -> Dict[str, Any]:
    return resp_json


@pytest.fixture
def post_resp_ok(post_resp_json) -> Mock:
    return create_resp(status_code=200, json_resp=post_resp_json)


@patch('lotame.lotame.requests')
def test_post_ok(mock_requests,
                 credentials,
                 service,
                 post_resp_ok,
                 post_resp_json):
    mock_requests.post.return_value = post_resp_ok

    api = Api(credentials=credentials)
    rsp = api.post(service=service)
    assert rsp == post_resp_json


@pytest.fixture
def put_req_json() -> Dict[str, Any]:
    return {'data1': 6, 'data2': 'Six', 'data3': 6.0}


@pytest.fixture
def put_resp_json(put_req_json) -> Dict[str, Any]:
    return put_req_json


@pytest.fixture
def put_resp_ok(put_resp_json) -> Mock:
    return create_resp(200, put_resp_json)


@patch('lotame.lotame.requests')
def test_put_ok(mock_requests,
                credentials,
                service,
                put_resp_ok,
                put_req_json,
                put_resp_json):
    mock_requests.put.return_value = put_resp_ok

    api = Api(credentials=credentials)
    rsp = api.put(service=service, body=put_req_json)
    assert rsp == put_resp_json


@pytest.fixture
def delete_resp_json(resp_json) -> Dict[str, Any]:
    return resp_json


@pytest.fixture
def delete_resp_ok(delete_resp_json) -> Mock:
    return create_resp(status_code=200, json_resp=delete_resp_json)


@patch('lotame.lotame.requests')
def test_delete_ok(mock_requests,
                   credentials,
                   service,
                   delete_resp_ok,
                   delete_resp_json):
    mock_requests.delete.return_value = delete_resp_ok

    api = Api(credentials=credentials)
    rsp = api.delete(service=service)
    assert rsp == delete_resp_json
