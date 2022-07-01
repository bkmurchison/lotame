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


@pytest.fixture()
def missing_fields_exc_message() -> str:
    return "Missing credentials. All client_id, token and access are required."


def test_credential_no_assignments(missing_fields_exc_message):
    do_exception_assertion(lambda: Credentials(), missing_fields_exc_message)


def test_credential_no_assignments_only_client_id_assigned(client_id,
                                                           missing_fields_exc_message):
    do_exception_assertion(
        lambda: Credentials(client_id=client_id),
        missing_fields_exc_message
    )


def test_credentials_with_client_id_not_assigned(token,
                                                 access,
                                                 base_url,
                                                 missing_fields_exc_message):
    do_exception_assertion(
        lambda: Credentials(token=token, access=access, base_url=base_url),
        missing_fields_exc_message
    )


def test_credential_no_assignments_only_token_assigned(token, missing_fields_exc_message):
    do_exception_assertion(lambda: Credentials(token=token),
                           missing_fields_exc_message)


def test_credentials_with_token_not_assigned(client_id,
                                             access,
                                             base_url,
                                             missing_fields_exc_message):
    do_exception_assertion(
        lambda: Credentials(client_id=client_id, access=access, base_url=base_url),
        missing_fields_exc_message)


def test_credential_no_assignments_only_access_assigned(access,
                                                        missing_fields_exc_message):
    do_exception_assertion(lambda: Credentials(access=access),
                           missing_fields_exc_message)


def test_credentials_with_access_not_assigned(client_id, token, base_url,
                                              missing_fields_exc_message):
    do_exception_assertion(lambda: Credentials(client_id=client_id, token=token, base_url=base_url),
                           missing_fields_exc_message)


def test_credential_no_assignments_only_base_url_assigned(base_url,
                                                          missing_fields_exc_message):
    do_exception_assertion(lambda: Credentials(base_url=base_url),
                           missing_fields_exc_message)


def do_exception_assertion(func_causing_assertion, err_message) -> None:
    with pytest.raises(Exception) as e:
        func_causing_assertion()
    assert str(e.value) == err_message


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
