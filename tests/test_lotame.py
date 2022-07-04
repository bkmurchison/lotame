"""
To be implemented.
"""
from __future__ import absolute_import
from __future__ import print_function

import itertools
import json
from unittest.mock import patch, call
from lotame.lotame import Credentials, Api
import pytest
import requests

try:
    from unittest.mock import MagicMock
except:
    from mock import MagicMock


"""
To be implemented
"""
@pytest.fixture()
def a_client_id():
    return "a_client_id"


@pytest.fixture()
def a_token():
    return "a_token"


@pytest.fixture()
def an_access():
    return "an_access"


@pytest.fixture()
def a_base_url():
    return "a_base_url"


def test_credentials(a_client_id, a_token, an_access, a_base_url):
    credentials = Credentials(a_client_id, a_token, an_access, a_base_url)

    assert credentials.client_id == a_client_id
    assert credentials.token == a_token
    assert credentials.access == an_access
    assert credentials.base_url == a_base_url


def test_credentials_with_defaulted_base_url(a_client_id, a_token, an_access):
    credentials = Credentials(a_client_id, a_token, an_access)

    assert credentials.client_id == a_client_id
    assert credentials.token == a_token
    assert credentials.access == an_access
    assert credentials.base_url == Credentials.DEFAULT_BASE_URL


def test_credentials_with_client_id_none(a_token, an_access):
    with pytest.raises(Exception) as e:
        Credentials(None, a_token, an_access)
    assert(str(e.value)
           == "Missing credentials. All client_id, token and access are required."
           )


def test_credentials_with_token_none(a_client_id, an_access):
    with pytest.raises(Exception) as e:
        Credentials(a_client_id, None, an_access)
    assert(str(e.value)
           == "Missing credentials. All client_id, token and access are required."
           )


def test_credentials_with_access_none(a_client_id, a_token):
    with pytest.raises(Exception) as e:
        Credentials(a_client_id, a_token, None)
    assert(str(e.value)
           == "Missing credentials. All client_id, token and access are required."
           )


@pytest.fixture()
def mock_credentials(a_token, an_access):
    with patch('lotame.lotame.Credentials') as c:
        yield c


def test_api(mock_credentials):
    api = Api(mock_credentials)

    assert api.credentials == mock_credentials


def test_api_defaulted_credentials():
    with pytest.raises(Exception) as e:
        api = Api()


def test_populate_url_params_defaulted_args(mock_credentials):
    url_params = Api(mock_credentials).populateUrlParams()
    assert url_params == "?="


@pytest.fixture()
def url_no_symbols():
    return Credentials.DEFAULT_BASE_URL


def test_populate_url_params_url_assigned_no_symbols(
        mock_credentials,
        url_no_symbols
):
    url_params = Api(mock_credentials).populateUrlParams(url_no_symbols)
    assert url_params == url_no_symbols + "?="


@pytest.fixture()
def param_0_key():
    return "a_key_0"


@pytest.fixture()
def param_0_val():
    return "a_val_0"


@pytest.fixture()
def param_0_str(param_0_key, param_0_val):
    return params_as_str(param_0_key, param_0_val)


def test_populate_url_params_with_params_url_assigned_no_symbols(
        mock_credentials,
        url_no_symbols,
        param_0_key,
        param_0_val
):
    exp_param_0_str = params_as_str(param_0_key, param_0_val)

    url_params = Api(mock_credentials).populateUrlParams(url_no_symbols,
                                                         param_0_key,
                                                         param_0_val)
    assert url_no_symbols in url_params
    assert exp_param_0_str in url_params
    assert "?" in url_params

    exp_param_0_idx = url_params.index("?") + 1
    assert url_params[exp_param_0_idx:] == exp_param_0_str


@pytest.fixture()
def param_1_key():
    return "a_key_1"


@pytest.fixture()
def param_1_val():
    return "a_val_1"


@pytest.fixture()
def param_1_str(param_0_key, param_0_val):
    return params_as_str(param_0_key, param_0_val)


@pytest.fixture()
def url_has_q_mark(url_no_symbols, param_0_str):
    return f"{url_no_symbols}?{param_0_str}"


def test_populate_url_params_url_assigned_has_q_mark(
        mock_credentials,
        url_has_q_mark,
        param_1_key,
        param_1_val,
        param_1_str
):
    exp_param_1_str = params_as_str(param_1_key, param_1_val)

    url_params = Api(mock_credentials).populateUrlParams(url_has_q_mark,
                                                         param_1_key,
                                                         param_1_val)
    assert url_has_q_mark in url_params
    assert exp_param_1_str in url_params
    assert "&" in url_params

    exp_param_1_idx = url_params.index("&") + 1
    assert url_params[exp_param_1_idx:] == exp_param_1_str


@pytest.fixture()
def mocked_credentials_with_client_id_and_default_base_url(mock_credentials,
                                                           a_client_id):
    mock_credentials.base_url = Credentials.DEFAULT_BASE_URL
    mock_credentials.client_id = a_client_id
    return mock_credentials


def test_build_url_defaulted_args(mocked_credentials_with_client_id_and_default_base_url,
                                  a_client_id):
    url = Api(mocked_credentials_with_client_id_and_default_base_url).buildUrl()
    assert url == ""


@pytest.fixture()
def a_service():
    return "/a/service"


def test_build_url_with_service_only(mocked_credentials_with_client_id_and_default_base_url,
                                     a_client_id,
                                     a_service):
    exp_client_id_str = params_as_str("client_id", a_client_id)

    url = Api(mocked_credentials_with_client_id_and_default_base_url).buildUrl(service=a_service)
    assert url == f"{Credentials.DEFAULT_BASE_URL}{a_service}?{exp_client_id_str}"


@pytest.fixture()
def param_0_as_dict(param_0_key, param_0_val):
    return {param_0_key: param_0_val}


def test_build_url_with_params_only(mocked_credentials_with_client_id_and_default_base_url,
                                    a_client_id,
                                    param_0_as_dict,
                                    param_0_str):
    url = Api(mocked_credentials_with_client_id_and_default_base_url).buildUrl(params=param_0_as_dict)
    assert url == ""


def test_build_url_with_service_and_params(mocked_credentials_with_client_id_and_default_base_url,
                                           a_client_id,
                                           a_service,
                                           param_0_as_dict,
                                           param_0_str):
    exp_client_id_str = params_as_str("client_id", a_client_id)

    url = Api(mocked_credentials_with_client_id_and_default_base_url).buildUrl(
        service=a_service,
        params=param_0_as_dict
    )
    assert url == f"{Credentials.DEFAULT_BASE_URL}{a_service}?{exp_client_id_str}&{param_0_str}"


@pytest.fixture()
def param_with_list_value_as_dict(param_0_key,
                                  param_0_val,
                                  param_1_val):
    return {param_0_key: [param_0_val, param_1_val]}


@pytest.fixture()
def param_with_list_value_as_str(param_with_list_value_as_dict):
    param_strs = [[f"{k}={v}" for v in vs] for k, vs in param_with_list_value_as_dict.items()]
    flat_param_strs = list(itertools.chain(*param_strs))
    return "&".join(flat_param_strs)


def test_build_url_with_service_and_param_as_list(
        mocked_credentials_with_client_id_and_default_base_url,
        a_client_id,
        a_service,
        param_with_list_value_as_dict,
        param_with_list_value_as_str):
    exp_client_id_str = params_as_str("client_id", a_client_id)

    url = Api(mocked_credentials_with_client_id_and_default_base_url).buildUrl(
        service=a_service,
        params=param_with_list_value_as_dict
    )
    assert(
            url
            == f"{Credentials.DEFAULT_BASE_URL}{a_service}?{exp_client_id_str}&{param_with_list_value_as_str}"
    )


def test_build_url_with_service_and_params_auto_assign_false(
        mocked_credentials_with_client_id_and_default_base_url,
        a_client_id,
        a_service,
        param_0_as_dict,
        param_0_str):

    url = Api(mocked_credentials_with_client_id_and_default_base_url).buildUrl(
        service=a_service,
        params=param_0_as_dict,
        auto_assign_client_id=False
    )
    assert url == f"{Credentials.DEFAULT_BASE_URL}{a_service}?{param_0_str}"


@pytest.fixture()
def mock_credentials_with_token_and_access(mock_credentials,
                                           a_token,
                                           an_access):
    mock_credentials.token = a_token
    mock_credentials.access = an_access

    return mock_credentials


def test_headers_no_base_headers_provided(mock_credentials_with_token_and_access):
    headers = Api(mock_credentials_with_token_and_access).mergeHeaders({})

    assert len(headers) == 2
    assert(
            headers["x-lotame-token"]
            == mock_credentials_with_token_and_access.token
    )
    assert(
            headers["x-lotame-access"]
            == mock_credentials_with_token_and_access.access
    )


@pytest.fixture()
def base_header_0_key():
    return "base-header-0"


@pytest.fixture()
def base_header_0_val():
    return "BaseHeader0Val"


@pytest.fixture()
def base_headers(base_header_0_key, base_header_0_val):
    return base_header_0_key, base_header_0_val


def test_headers_base_headers_provided(mock_credentials_with_token_and_access,
                                       base_headers):
    headers = Api(mock_credentials_with_token_and_access).mergeHeaders(
        dict([base_headers])
    )

    assert len(headers) == 3
    assert(
            headers["x-lotame-token"]
            == mock_credentials_with_token_and_access.token
    )
    assert(
            headers["x-lotame-access"]
            == mock_credentials_with_token_and_access.access
    )
    assert headers[base_headers[0]] == base_headers[1]


def params_as_str(key, val):
    return f"{key}={val}"


def test_perform_request_defaulted_arg(mock_credentials_with_token_and_access):
    resp = Api(mock_credentials_with_token_and_access).performRequest()
    assert resp == "Invalid request type"


def test_perform_request_service_arg_only(mock_credentials_with_token_and_access,
                                          a_service):
    resp = Api(mock_credentials_with_token_and_access).performRequest(service=a_service)
    assert resp == "Invalid request type"


@pytest.fixture()
def invalid_request_type():
    return "invalid_req_type"


def test_perform_request_service_and_invalid_type(
        mock_credentials_with_token_and_access,
        a_service,
        invalid_request_type
):
    resp = Api(mock_credentials_with_token_and_access).performRequest(
        service=a_service,
        type=invalid_request_type
    )
    assert resp == "Invalid request type"


@pytest.fixture()
def perform_request_expected_headers(a_token, an_access):
    return {"x-lotame-token": a_token, "x-lotame-access": an_access}


@pytest.fixture()
def perform_requests_expected_response_data():
    return {}


@pytest.fixture()
def perform_requests_expected_response(perform_requests_expected_response_data):
    with patch.object(requests, 'Response') as r:
        r.json.return_value = perform_requests_expected_response_data
        yield r


@pytest.fixture()
def mock_requests_base():
    with patch('lotame.lotame.requests') as r:
        yield r


@pytest.fixture()
def mock_requests_get(mock_requests_base,
                      perform_requests_expected_response):
    mock_requests_base.get.return_value = perform_requests_expected_response
    return mock_requests_base


def test_perform_request_service_and_request_get(
        mock_requests_get,
        mock_credentials_with_token_and_access,
        a_service,
        a_token,
        an_access,
        perform_request_expected_headers,
        perform_requests_expected_response
):
    resp = Api(mock_credentials_with_token_and_access).performRequest(
        service=a_service,
        type=Api.REQUEST_GET
    )
    assert resp == perform_requests_expected_response

    calls = [call(a_service, headers=perform_request_expected_headers)]
    mock_requests_get.get.assert_has_calls(calls)


@pytest.fixture()
def request_body():
    return {}


@pytest.fixture()
def mock_requests_post(mock_requests_base,
                       perform_requests_expected_response):
    mock_requests_base.post.return_value = perform_requests_expected_response
    return mock_requests_base


def test_perform_request_service_and_request_post_body(
        mock_requests_post,
        mock_credentials_with_token_and_access,
        a_service,
        request_body,
        perform_request_expected_headers,
        perform_requests_expected_response
):
    resp = Api(mock_credentials_with_token_and_access).performRequest(
        service=a_service,
        type=Api.REQUEST_POSTBODY,
        body=request_body
    )
    assert resp == perform_requests_expected_response

    calls = [call(a_service,
                  data=json.dumps(request_body),
                  headers=perform_request_expected_headers)]
    mock_requests_post.post.assert_has_calls(calls)


def test_perform_request_service_and_request_post(
        mock_requests_post,
        mock_credentials_with_token_and_access,
        a_service,
        a_token,
        an_access,
        perform_request_expected_headers,
        perform_requests_expected_response
):
    resp = Api(mock_credentials_with_token_and_access).performRequest(
        service=a_service,
        type=Api.REQUEST_POST
    )
    assert resp == perform_requests_expected_response

    calls = [call(a_service, headers=perform_request_expected_headers)]
    mock_requests_post.post.assert_has_calls(calls)


@pytest.fixture()
def mock_requests_put(mock_requests_base,
                      perform_requests_expected_response):
    mock_requests_base.put.return_value = perform_requests_expected_response
    return mock_requests_base


def test_perform_request_service_and_request_put(
        mock_requests_put,
        mock_credentials_with_token_and_access,
        a_service,
        request_body,
        perform_request_expected_headers,
        perform_requests_expected_response
):
    resp = Api(mock_credentials_with_token_and_access).performRequest(
        service=a_service,
        type=Api.REQUEST_PUT,
        body=request_body
    )
    assert resp == perform_requests_expected_response

    calls = [call(a_service,
                  data=json.dumps(request_body),
                  headers=perform_request_expected_headers)]
    mock_requests_put.put.assert_has_calls(calls)


@pytest.fixture()
def mock_requests_delete(mock_requests_base,
                         perform_requests_expected_response):
    mock_requests_base.delete.return_value = perform_requests_expected_response
    return mock_requests_base


def test_perform_request_service_and_request_delete(
        mock_requests_delete,
        mock_credentials_with_token_and_access,
        a_service,
        request_body,
        perform_request_expected_headers,
        perform_requests_expected_response
):
    resp = Api(mock_credentials_with_token_and_access).performRequest(
        service=a_service,
        type=Api.REQUEST_DELETE
    )
    assert resp == perform_requests_expected_response

    calls = [call(a_service,
                  headers=perform_request_expected_headers)]
    mock_requests_delete.delete.assert_has_calls(calls)


@patch.object(Api, 'performRequest')
def test_get(mock_perform_request,
             mock_credentials,
             a_service,
             perform_requests_expected_response,
             perform_requests_expected_response_data):
    mock_perform_request.return_value = perform_requests_expected_response
    resp = Api(mock_credentials).get(a_service)
    assert resp == perform_requests_expected_response_data

    calls = [call(service=a_service,
                  user=None,
                  access=None,
                  type=Api.REQUEST_GET,
                  headers=Api.DEFAULT_JSON_RECEIVE_HEADER)]
    mock_perform_request.assert_has_calls(calls)


@patch.object(Api, 'performRequest')
def test_post_body(mock_perform_request,
                   mock_credentials,
                   a_service,
                   request_body,
                   perform_requests_expected_response,
                   perform_requests_expected_response_data):
    mock_perform_request.return_value = perform_requests_expected_response
    resp = Api(mock_credentials).postBody(service=a_service,
                                          body=request_body)
    assert resp == perform_requests_expected_response_data

    calls = [call(service=a_service,
                  user=None,
                  access=None,
                  type=Api.REQUEST_POSTBODY,
                  headers=Api.DEFAULT_JSON_SEND_HEADER,
                  body=request_body)]
    mock_perform_request.assert_has_calls(calls)


@patch.object(Api, 'performRequest')
def test_post(mock_perform_request,
              mock_credentials,
              a_service,
              request_body,
              perform_requests_expected_response,
              perform_requests_expected_response_data):
    mock_perform_request.return_value = perform_requests_expected_response
    resp = Api(mock_credentials).post(service=a_service)
    assert resp == perform_requests_expected_response_data

    calls = [call(service=a_service,
                  user=None,
                  access=None,
                  type=Api.REQUEST_POST,
                  headers=Api.DEFAULT_JSON_SEND_HEADER)]
    mock_perform_request.assert_has_calls(calls)


@patch.object(Api, 'performRequest')
def test_put(mock_perform_request,
             mock_credentials,
             a_service,
             request_body,
             perform_requests_expected_response,
             perform_requests_expected_response_data):
    mock_perform_request.return_value = perform_requests_expected_response
    resp = Api(mock_credentials).put(service=a_service, body=request_body)
    assert resp == perform_requests_expected_response_data

    calls = [call(service=a_service,
                  user=None,
                  access=None,
                  type=Api.REQUEST_PUT,
                  headers=Api.DEFAULT_JSON_SEND_HEADER,
                  body=request_body)]
    mock_perform_request.assert_has_calls(calls)


@patch.object(Api, 'performRequest')
def test_delete(mock_perform_request,
                mock_credentials,
                a_service,
                request_body,
                perform_requests_expected_response,
                perform_requests_expected_response_data):
    mock_perform_request.return_value = perform_requests_expected_response
    resp = Api(mock_credentials).delete(service=a_service)
    assert resp == perform_requests_expected_response_data

    calls = [call(service=a_service,
                  user=None,
                  access=None,
                  type=Api.REQUEST_DELETE,
                  headers=Api.DEFAULT_JSON_RECEIVE_HEADER)]
    mock_perform_request.assert_has_calls(calls)
