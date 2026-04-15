"""Platzhalter fuer spaetere Keycloak-Befuellung im DEV-Modus."""

from loguru import logger

from carrier.config.dev_modus import dev_keycloak_populate

__all__ = [
    "KeycloakPopulateService",
    "get_keycloak_populate_service",
    "keycloak_populate",
]


class KeycloakPopulateService:
    """No-op-Service, bis fachliche Security-Logik vorhanden ist."""

    def populate(self) -> None:
        """Führt das Laden der Keycloak-Beispieldaten aus."""
        logger.info("Keycloak-Populate uebersprungen: noch nicht implementiert")


def get_keycloak_populate_service() -> KeycloakPopulateService:
    """Factory-Funktion fuer KeycloakPopulateService."""
    return KeycloakPopulateService()


def keycloak_populate() -> None:
    """Keycloak im DEV-Modus optional vorbereiten."""
    if dev_keycloak_populate:
        get_keycloak_populate_service().populate()
