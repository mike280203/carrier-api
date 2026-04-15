"""Allgemeine Daten für die Integrationstests."""

from http import HTTPStatus
from pathlib import Path
from ssl import create_default_context
from typing import Final

from httpx import post

__all__ = [
    "base_url",
    "ctx",
    "graphql_url",
    "health_url",
    "login",
    "password_admin",
    "password_user",
    "rest_url",
    "timeout",
    "token_path",
    "username_admin",
    "username_user",
]

schema: Final = "https"
port: Final = 8000
host: Final = "127.0.0.1"
base_url: Final = f"{schema}://{host}:{port}"

rest_url: Final = f"{base_url}/rest/carriers"
graphql_url: Final = f"{base_url}/graphql"
health_url: Final = f"{base_url}/health"
token_path: Final = "/auth/token"  # noqa: S105

username_admin: Final = "admin"
password_admin: Final = "p"  # noqa: S105  # NOSONAR

username_user: Final = "carrier"
password_user: Final = "p"  # noqa: S105  # NOSONAR

timeout: Final = 5

certificate: Final = str(Path("tests") / "integration" / "certificate.crt")
ctx = create_default_context(cafile=certificate)


def login(
    username: str = username_admin,
    password: str = password_admin,  # NOSONAR
) -> str:
    """Token über die REST-Schnittstelle abrufen."""
    login_data: Final = {"username": username, "password": password}
    response: Final = post(
        f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"login() mit Statuscode {response.status_code}")
    response_body: Final = response.json()
    token: Final = response_body.get("token")
    if token is None or not isinstance(token, str):
        raise RuntimeError(f"login() mit ungueltigem Token: type={type(token)}")
    return token
