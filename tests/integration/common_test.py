"""Allgemeine Daten für Integrationstests."""

from pathlib import Path
from ssl import create_default_context
from typing import Final

__all__ = [
    "base_url",
    "ctx",
    "graphql_url",
    "health_url",
    "rest_url",
    "timeout",
]

schema: Final = "https"
port: Final = 8000
host: Final = "127.0.0.1"
base_url: Final = f"{schema}://{host}:{port}"

rest_url: Final = f"{base_url}/rest/carriers"
graphql_url: Final = f"{base_url}/graphql"
health_url: Final = f"{base_url}/health"

timeout: Final = 5

certificate: Final = str(Path("tests") / "integration" / "certificate.crt")
ctx = create_default_context(cafile=certificate)
