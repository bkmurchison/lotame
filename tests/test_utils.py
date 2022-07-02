from _ast import List
from typing import Tuple, Dict, Any
from unittest.mock import patch

import pytest

from lotame import populate_url_params, build_url, Credentials
from tests.fixtures import client_id, token, access, base_url

@pytest.fixture
def base_url() -> str:
    return "s3://this/is/the/path/to/the/directory"


@pytest.fixture
def the_param_key() -> str:
    return "param_1st_key"


@pytest.fixture
def the_param_val() -> str:
    return "param_1st_val"


@pytest.fixture
def empty_url_param_str() -> str:
    return ""


@pytest.fixture
def the_key_val_param_tuple(the_param_key, the_param_val) -> Tuple[str, str]:
    return the_param_key, the_param_val


@pytest.fixture
def the_key_val_param_dict(the_key_val_param_tuple) -> Dict[str, str]:
    the_param_key, the_param_val = the_key_val_param_tuple
    return {the_param_key: the_param_val}


@pytest.fixture
def the_key_val_param_str(the_key_val_param_tuple) -> str:
    the_param_key, the_param_val = the_key_val_param_tuple
    return f"{the_param_key}={the_param_val}"


@pytest.fixture
def the_test_url_params_single_set_params(base_url,
                                          the_key_val_param_str) -> str:
    return f"{base_url}?{the_key_val_param_str}"


@pytest.fixture
def the_second_param_key() -> str:
    return "param_2nd_key"


@pytest.fixture
def the_second_param_val() -> str:
    return "param_2nd_val"


@pytest.fixture
def the_second_key_val_param(the_second_param_key, the_second_param_val) -> str:
    return f"{the_second_param_key}={the_second_param_val}"


@pytest.fixture
def the_test_url_params_with_second_set_params(the_test_url_params_single_set_params,
                                               the_second_key_val_param) -> str:
    return f"{the_test_url_params_single_set_params}&{the_second_key_val_param}"


def test_populate_url_params_url_is_none_args_defaulted():
    with pytest.raises(Exception) as e:
        populate_url_params(None)
    str(e.value) == "Missing URL value. URL is required."


def test_populate_url_params_defaulted_args(base_url):
    u = populate_url_params(base_url)
    assert u == base_url


def test_populate_url_params_none_arg(base_url):
    u = populate_url_params(base_url, key=None, val=None)
    assert u == base_url


def test_populate_url_params_key_is_none(base_url, the_param_val):
    u = populate_url_params(base_url, key=None, val=the_param_val)
    assert u == base_url


def test_populate_url_params_key_is_defaulted(base_url, the_param_val):
    u = populate_url_params(base_url, val=the_param_val)
    assert u == base_url


def test_populate_url_params_val_is_defaulted(base_url, the_param_key):
    u = populate_url_params(base_url, key=the_param_key)
    assert u == base_url


def test_populate_url_params_first_key_val_set(base_url,
                                               the_param_key,
                                               the_param_val,
                                               the_key_val_param_str,
                                               the_test_url_params_single_set_params):
    u = populate_url_params(base_url, key=the_param_key, val=the_param_val)
    assert "?" in u
    begin_params_symbol_idx = u.index("?")
    assert the_key_val_param_str in u
    assert begin_params_symbol_idx == len(base_url)
    assert u[begin_params_symbol_idx + 1:] == the_key_val_param_str
    assert u == the_test_url_params_single_set_params


def test_populate_url_params_second_key_val_set(the_test_url_params_single_set_params,
                                                the_second_param_key,
                                                the_second_param_val,
                                                the_second_key_val_param,
                                                the_test_url_params_with_second_set_params):
    u = populate_url_params(the_test_url_params_single_set_params,
                            key=the_second_param_key,
                            val=the_second_param_val)
    assert "&" in u
    second_params_symbol_idx = u.rindex("&")
    assert the_second_key_val_param in u
    assert second_params_symbol_idx == len(the_test_url_params_single_set_params)
    assert u[second_params_symbol_idx + 1:] == the_second_key_val_param
    assert u == the_test_url_params_with_second_set_params


@pytest.fixture
def credentials(client_id, token, access, base_url) -> Credentials:
    return Credentials(client_id=client_id,
                       token=token,
                       access=access,
                       base_url=base_url)


def test_build_url_defaulted_args(credentials):
    u = build_url(credentials)
    assert u == ""


@pytest.fixture
def service() -> str:
    return "/a/fake/service"


@pytest.fixture
def client_id_param_str(client_id) -> str:
    return f"client_id={client_id}"


@patch('lotame.utils.Credentials')
def test_build_url_with_service(mock_credentials,
                                service,
                                client_id,
                                base_url,
                                client_id_param_str):
    mock_credentials.base_url = base_url
    mock_credentials.client_id = client_id

    u = build_url(mock_credentials, service=service)

    assert service in u
    assert "?" in u
    assert client_id_param_str in u


@patch('lotame.utils.Credentials')
def test_build_url_with_service_and_params(mock_credentials,
                                           service,
                                           client_id,
                                           base_url,
                                           the_key_val_param_str,
                                           the_key_val_param_dict):
    mock_credentials.base_url = base_url
    mock_credentials.client_id = client_id

    u = build_url(mock_credentials, service=service, params=the_key_val_param_dict)

    assert "&" in u
    assert the_key_val_param_str in u


@pytest.fixture
def the_key_list_val_param_dict(the_param_key,
                                the_param_val,
                                the_second_param_val) -> Dict[str, Any]:
    return {the_param_key: [the_param_val, the_second_param_val]}


@pytest.fixture
def the_key_list_val_param_str(the_param_key,
                               the_param_val,
                               the_second_param_val) -> str:
    return f"{the_param_key}={the_param_val}&{the_param_key}={the_second_param_val}"


@patch('lotame.utils.Credentials')
def test_build_url_with_service_and_list_params(mock_credentials,
                                                service,
                                                client_id,
                                                base_url,
                                                the_key_list_val_param_str,
                                                the_key_list_val_param_dict):
    mock_credentials.base_url = base_url
    mock_credentials.client_id = client_id

    u = build_url(mock_credentials, service=service, params=the_key_list_val_param_dict)

    assert the_key_list_val_param_str in u
