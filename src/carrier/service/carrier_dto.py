"""DTO-Klasse für Carrier, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

from carrier.entity import Carrier
from carrier.service.commandcenter_dto import CommandCenterDTO

__all__ = ["CarrierDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class CarrierDTO:
    """DTO-Klasse für Carrier, insbesondere ohne Decorators für SQLAlchemy."""

    id: int
    version: int
    name: str
    nation: str
    carrier_type: str
    commandcenter: CommandCenterDTO

    def __init__(self, carrier: Carrier) -> None:
        """Initialisierung von CarrierDTO durch ein Objekt von Carrier."""
        carrier_id = carrier.id
        self.id = carrier_id if carrier_id is not None else -1
        self.version = carrier.version
        self.name = carrier.name
        self.nation = carrier.nation
        self.carrier_type = carrier.carrier_type.value
        self.commandcenter = CommandCenterDTO(commandcenter=carrier.commandcenter)
