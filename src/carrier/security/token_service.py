"""Anwendungskern für Benutzerdaten."""

from collections.abc import Mapping
from dataclasses import asdict
from typing import Any, Final

from fastapi import Request
from jwcrypto.common import JWException
from keycloak import KeycloakOpenID
from loguru import logger

from carrier.config import keycloak_config
from carrier.security.exceptions import AuthorizationError
from carrier.security.role import Role
from carrier.security.user import User

__all__ = ["TokenService"]


class TokenService:
    """Schnittstelle für das Management der Tokens von Keycloak."""

    def __init__(self) -> None:
        """Initialisierung der Schnittstelle zu Keycloak."""
        self.keycloak = KeycloakOpenID(**asdict(keycloak_config))

    def _get_token_from_request(self, request: Request) -> str:
        """Den Token aus "Authorization"-String im Request-Header extrahieren.

        :param request: Request-Objekt von FastAPI mit codiertem "Authorization"-String
                        einschließlich Bearer
        :return: String nach 'Bearer' im Authorization-Header
        :rtype: str
        :raises: AuthorizationError, falls der Authorization_Header syntaktisch falsch
        ist.
        """
        authorization_header: Final = request.headers.get("Authorization")
        logger.debug("authorization_header={}", authorization_header)
        if authorization_header is None:
            raise AuthorizationError

        try:
            authorization_scheme, bearer_token = authorization_header.split()
        except ValueError as err:
            raise AuthorizationError from err
        if authorization_scheme.lower() != "bearer":
            raise AuthorizationError
        return bearer_token

    def get_user_from_token(self, token: str) -> User:
        """Die User-Daten aus dem codierten Token extrahieren.

        :param token: Token als String
        :return: User-Daten mit Benutzername und Rollen
        :rtype: User
        :raises AuthorizationError: Falls keine User-Daten extrahiert werden können
        """
        try:
            token_decoded: Final = self.keycloak.decode_token(token=token)
        except JWException as err:
            raise AuthorizationError from err

        logger.debug("token_decoded={}", token_decoded)
        username: Final[str] = token_decoded["preferred_username"]
        roles = self.get_roles_from_token(token_decoded)

        user = User(
            username=username,
            roles=roles,
        )
        logger.debug("user={}", user)
        return user

    def get_user_from_request(self, request: Request) -> User:
        """Die User-Daten aus dem codierten "Authorization"-String extrahieren.

        :param request: Request-Objekt von FastAPI mit codiertem "Authorization"-String
                        einschließlich Bearer
        :return: User-Daten mit Benutzername und Rollen
        :rtype: User
        """
        bearer_token: Final = self._get_token_from_request(request)
        user: Final = self.get_user_from_token(token=bearer_token)
        logger.debug("user={}", user)
        return user

    def get_roles_from_token(self, token: str | Mapping[str, Any]) -> list[Role]:
        """Aus einem Access Token von Keycloak die zugehörigen Rollen extrahieren.

        :param token: Zu überprüfender Token
        :return: Liste der Rollen
        :rtype: list[str]
        """
        if isinstance(token, str):
            token_decoded = self.keycloak.decode_token(token=token)
        else:
            token_decoded = token
        logger.debug("token_decoded={}", token_decoded)

        roles: Final[str] = token_decoded["resource_access"][self.keycloak.client_id][
            "roles"
        ]
        roles_enum: Final = [Role[role.upper()] for role in roles]
        logger.debug("roles_enum={}", roles_enum)
        return roles_enum

    def token(self, username: str, password: str) -> dict[str, Any]:
        """Einen Access Token von Keycloak anfordern.

        :param username: Benutzername
        :param password: Passwort
        :return: Token-Daten von Keycloak
        :rtype: dict[str, Any]
        :raises RuntimeError: Falls Login bei Keycloak fehlschlägt
        """
        logger.debug("username={}", username)
        try:
            token_data: Final = self.keycloak.token(
                username=username,
                password=password,
            )
        except Exception as ex:
            logger.exception("Login bei Keycloak fehlgeschlagen: username={}", username)
            raise RuntimeError("Login bei Keycloak fehlgeschlagen") from ex

        logger.debug("token_data keys={}", list(token_data.keys()))
        return token_data
