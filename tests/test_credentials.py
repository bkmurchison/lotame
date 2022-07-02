from functools import partial

import pytest

from lotame.credentials import Credentials
from tests.fixtures import client_id, token, access, base_url


@pytest.fixture()
def none_value() -> None:
    return None


def missing_fields_exc_message(*args) -> str:
    return f"Missing credentials. {','.join(args)} required."


@pytest.fixture()
def client_id_fld():
    return "client_id"


@pytest.fixture()
def token_fld():
    return "token"


@pytest.fixture()
def access_fld():
    return "access"


def test_credential_no_assignments(client_id_fld,
                                   token_fld,
                                   access_fld):
    do_exception_assertion(lambda: Credentials(),
                           missing_fields_exc_message(client_id_fld, token_fld, access_fld))


def test_credential_no_assignments_only_client_id_assigned(client_id,
                                                           token_fld,
                                                           access_fld):
    do_exception_assertion(lambda: Credentials(client_id=client_id),
                           missing_fields_exc_message(token_fld, access_fld))


def test_credentials_with_client_id_not_assigned(token,
                                                 access,
                                                 base_url,
                                                 client_id_fld):
    do_exception_assertion(
        lambda: Credentials(token=token, access=access, base_url=base_url),
        missing_fields_exc_message(client_id_fld)
    )


def test_credential_no_assignments_only_token_assigned(token,
                                                       client_id_fld,
                                                       access_fld):
    do_exception_assertion(lambda: Credentials(token=token),
                           missing_fields_exc_message(client_id_fld, access_fld))


def test_credentials_with_token_not_assigned(client_id,
                                             access,
                                             base_url,
                                             token_fld):
    do_exception_assertion(
        lambda: Credentials(client_id=client_id, access=access, base_url=base_url),
        missing_fields_exc_message(token_fld))


def test_credential_no_assignments_only_access_assigned(access,
                                                        client_id_fld,
                                                        token_fld):
    do_exception_assertion(lambda: Credentials(access=access),
                           missing_fields_exc_message(client_id_fld, token_fld))


def test_credentials_with_access_not_assigned(client_id, token, base_url,
                                              access_fld):
    do_exception_assertion(lambda: Credentials(client_id=client_id, token=token, base_url=base_url),
                           missing_fields_exc_message(access_fld))


def test_credential_no_assignments_only_base_url_assigned(base_url,
                                                          client_id_fld,
                                                          access_fld,
                                                          token_fld):
    do_exception_assertion(lambda: Credentials(base_url=base_url),
                           missing_fields_exc_message(client_id_fld, token_fld, access_fld))


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
