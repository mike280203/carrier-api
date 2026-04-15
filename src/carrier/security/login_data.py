"""Data class für die Login-Daten."""

from dataclasses import dataclass

__all__ = ["LoginData"]


@dataclass
class LoginData:
    """Daten für den Login."""

    username: str
    """Benutzername"""

    password: str
    """Passwort"""

    class Config:
        """Konfiguration für die Datenklasse."""

        json_schema_extra = {
            "example": [
                {
                    "username": "admin",
                    "password": "p",
                },
            ],
        }
