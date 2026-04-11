"""Exceptions für die Carrier-Service-Schicht."""

from typing import Final

__all__ = [
    "CarrierNameExistsError",
    "CarrierNotFoundError",
    "CarrierServiceError",
]


class CarrierServiceError(Exception):
    """Basisklasse für fachliche Fehler in der Service-Schicht."""


class CarrierNotFoundError(CarrierServiceError):
    """Fehler, wenn kein Carrier zur angefragten ID existiert."""

    def __init__(self, carrier_id: int) -> None:
        """Initialisierung mit der nicht gefundenen Carrier-ID."""
        self.carrier_id = carrier_id
        message: Final = f"Kein Carrier mit der ID {carrier_id} gefunden."
        super().__init__(message)


class CarrierNameExistsError(CarrierServiceError):
    """Fehler, wenn ein Carrier-Name bereits vergeben ist."""

    def __init__(self, name: str) -> None:
        """Initialisierung mit dem bereits vorhandenen Namen."""
        self.name = name
        message: Final = f"Ein Carrier mit dem Namen '{name}' existiert bereits."
        super().__init__(message)

# versioning exceptions
