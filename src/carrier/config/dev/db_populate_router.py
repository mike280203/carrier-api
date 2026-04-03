"""Controller zum Neuladen der Entwicklungsdatenbank."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from carrier.config.dev.db_populate import DbPopulateService, get_db_populate_service

__all__ = ["router"]


router: Final = APIRouter(prefix="/db")


@router.post("/populate")
def populate(
    service: Annotated[DbPopulateService, Depends(get_db_populate_service)],
) -> JSONResponse:
    """Die DB im Entwicklungsmodus neu aufbauen."""
    service.populate()
    return JSONResponse(content={"db_populate": "success"})
