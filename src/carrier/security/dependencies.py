"""Factory-Funktionen für Dependency Injection."""

from carrier.security.token_service import TokenService

_token_service = TokenService()  # Singleton-Objekt


def get_token_service() -> TokenService:
    """Factory-Funktion für TokenService."""
    return _token_service
