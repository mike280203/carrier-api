"""DTO-Klasse für Commandcenter, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

from carrier.entity import CommandCenter


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class CommandCenterDTO:
    """DTO-Klasse für CommandCenter, insbesondere ohne Decorators für SQLAlchemy."""

    code_name: str
    security_level: int

    def __init__(self, commandcenter: CommandCenter) -> None:
        """Initialisierung von CommandCenterDTO durch ein Objekt von Commandcenter."""
        self.code_name = commandcenter.code_name
        self.security_level = commandcenter.security_level
