from lotame.lotame import Credentials
import pytest

try:
    from unittest.mock import MagicMock
except:
    from mock import MagicMock


@pytest.fixture()
def none_value() -> None:
    return None


@pytest.fixture()
def client_id() -> str:
    return "clientId"


@pytest.fixture()
def token() -> str:
    return "token"


@pytest.fixture()
def access() -> str:
    return "access"


@pytest.fixture()
def base_url() -> str:
    return "base_url"


def test_credential_with_client_id_assigned_none(none_value, token, access, base_url):
    with pytest.raises(Exception) as e:
        Credentials(client_id=none_value, token=token, access=access, base_url=base_url)
    assert(
            str(e.value) ==
            "Missing credentials. All client_id, token and access are required."
    )


def test_credentials_with_token_assigned_none(client_id, none_value, access, base_url):
    with pytest.raises(Exception) as e:
        Credentials(client_id=client_id, token=none_value, access=access, base_url=base_url)
    assert(
            str(e.value) ==
            "Missing credentials. All client_id, token and access are required."
    )


def test_credentials_with_access_assigned_none(client_id, token, none_value, base_url):
    with pytest.raises(Exception) as e:
        Credentials(client_id=client_id, token=token, access=none_value, base_url=base_url)
    assert(
            str(e.value) ==
            "Missing credentials. All client_id, token and access are required."
    )


def test_credentials_with_base_url_assigned_none(client_id, token, access, none_value):
    credentials = Credentials(client_id=client_id, token=token, access=access, base_url=none_value)
    assert credentials.client_id == client_id
    assert credentials.token == token
    assert credentials.access == access
    assert credentials.base_url == Credentials.DEFAULT_BASE_URL


def test_credentials_with_base_url_not_assigned(client_id, token, access):
    credentials = Credentials(client_id=client_id, token=token, access=access)
    assert credentials.client_id == client_id
    assert credentials.token == token
    assert credentials.access == access
    assert credentials.base_url == Credentials.DEFAULT_BASE_URL


def test_credentials_with_base_url_assigned(client_id, token, access, base_url):
    creds = Credentials(client_id=client_id, token=token, access=access, base_url=base_url)
    assert creds.client_id == client_id
    assert creds.token == token
    assert creds.access == access
    assert creds.base_url == base_url
