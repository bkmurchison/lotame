import pytest


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
    return "file://here/is/a/base/url"
