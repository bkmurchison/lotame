from typing import Any, Dict

from lotame.credentials import Credentials


def populate_url_params(url: str,
                        key: Any = "",
                        val: Any = "") -> str:
    if not url:
        raise Exception("Missing URL value. URL is required.")

    if key and val:
        if "?" not in url:
            url = url + "?"
        else:
            url = url + "&"

        url = url + str(key) + "=" + str(val)
    return url


def build_url(credentials: Credentials,
              service: str = "",
              params: Dict[Any, Any] = None,
              auto_assign_client_id: bool = True) -> str:
    if service == "":
        return service

    if params is None:
        params = {}

    url = credentials.base_url + service
    if auto_assign_client_id is True:
        url = url + "?client_id=" + str(credentials.client_id)
    for key, val in params.items():
        if isinstance(val, list):
            for v in val:
                url = populate_url_params(url, key, v)
        else:
            url = populate_url_params(url, key, val)
    return url
