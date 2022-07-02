from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Credentials:
    DEFAULT_BASE_URL = 'https://api.lotame.com/2'

    client_id: int = field(default=None)
    token: str = field(default=None)
    access: str = field(default=None)
    base_url: str = field(default=DEFAULT_BASE_URL)

    def __post_init__(self) -> None:
        missing_fields = []
        if not self.client_id:
            missing_fields.append('client_id')

        if not self.token:
            missing_fields.append('token')

        if not self.access:
            missing_fields.append('access')

        if missing_fields:
            raise Exception(f"Missing credentials. {','.join(missing_fields)} required.")
