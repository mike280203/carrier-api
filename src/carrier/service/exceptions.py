"""Exceptions für die Carrier-Service-Schicht."""

from typing import Final

__all__ = [
    "CarrierNameExistsError",
    "CarrierNotFoundError",
    "CarrierServiceError",
    "PreconditionFailedError",
    "PreconditionRequiredError",
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


class PreconditionRequiredError(CarrierServiceError):
    """Fehler, wenn für eine Änderung ein erforderlicher Header fehlt."""

    def __init__(self) -> None:
        """Initialisierung mit Standardmeldung für fehlendes If-Match."""
        message: Final = "Der Header 'If-Match' ist erforderlich."
        super().__init__(message)


class PreconditionFailedError(CarrierServiceError):
    """Fehler, wenn die Version im If-Match-Header nicht passt."""

    def __init__(self, expected_version: int, actual_value: str | None) -> None:
        """Initialisierung mit erwarteter Version und gelieferter Header-Angabe."""
        self.expected_version = expected_version
        self.actual_value = actual_value
        message: Final = (
            "Die Versionsangabe im Header 'If-Match' passt nicht zur "
            f"aktuellen Version {expected_version}."
        )
        super().__init__(message)
