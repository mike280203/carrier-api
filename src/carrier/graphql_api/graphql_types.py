"""Schema für GraphQL."""

import strawberry

from carrier.entity.carrier_type import CarrierType

__all__ = [
    "AircraftInput",
    "CarrierInput",
    "CommandCenterInput",
    "CreatePayload",
    "Suchparameter",
]


@strawberry.input
class Suchparameter:
    """Suchparameter für die Suche nach Carrier."""

    name: str | None = None
    """Name als Suchparameter"""

    nation: str | None = None
    """Nation als Suchparameter"""

    carrier_type: CarrierType | None = None
    """CarrierType als Suchparameter"""


@strawberry.input
class AircraftInput:
    """Aircraft zu einem neuen Carrier."""

    model: str
    """Modell des Aircraft"""

    manufacturer: str
    """Hersteller des Aircraft"""


@strawberry.input
class CommandCenterInput:
    """CommandCenter zu einem neuen Carrier."""

    code_name: str
    """Codename des CommandCenters."""

    security_level: int
    """Sicherheitsstufe des CommandCenters."""


@strawberry.input
class CarrierInput:
    """Daten für einen neuen Carrier."""

    name: str
    """Name des Carriers."""

    nation: str
    """Nation des Carriers."""

    carrier_type: CarrierType
    """Carrier-Typ."""

    commandcenter: CommandCenterInput
    """Zugehöriges CommandCenter."""

    aircrafts: list[AircraftInput]
    """Liste der Aircrafts."""


@strawberry.type
class CreatePayload:
    """Resultat-Typ, wenn ein neuer Carrier angelegt wurde."""

    id: int
    """ID des neu angelegten Carriers."""


@strawberry.type
class LoginResult:
    """Resultat-Typ, wenn ein Login erfolgreich war."""

    token: str
    """Token des eingeloggten Users."""

    expiresIn: str  # noqa: N815  # NOSONAR
    """Gültigkeitsdauer."""
    roles: list[str]
    """Rollen des Users."""
