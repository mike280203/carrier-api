"""Controller fuer eine spaetere Keycloak-Befuellung."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from carrier.config.dev.keycloak_populate import (
    KeycloakPopulateService,
    get_keycloak_populate_service,
)

__all__ = ["router"]


router: Final = APIRouter(prefix="/keycloak")


@router.post("/populate")
def populate(
    service: Annotated[KeycloakPopulateService, Depends(get_keycloak_populate_service)],
) -> JSONResponse:
    """Keycloak-Daten im Entwicklungsmodus vorbereiten."""
    service.populate()
    return JSONResponse(content={"keycloak_populate": "skipped"})
