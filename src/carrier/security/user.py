"""Entity-Klasse für Benutzerdaten."""

from dataclasses import dataclass

from carrier.security.role import Role


@dataclass()
class User:
    """Entity-Klasse für Benutzerdaten."""

    username: str
    """Benutzername."""

    roles: list[Role]
    """Rollen als Liste von Enums."""
