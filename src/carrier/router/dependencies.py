"""Factory-Funktionen für Dependency Injection im Carrier-Router."""

from typing import Annotated

from fastapi import Depends

from carrier.repository.carrier_repository import CarrierRepository
from carrier.service.carrier_service import CarrierService
from carrier.service.carrier_write_service import CarrierWriteService


def get_repository() -> CarrierRepository:
    """Factory-Funktion für CarrierRepository."""
    return CarrierRepository()


def get_service(
    repo: Annotated[CarrierRepository, Depends(get_repository)],
) -> CarrierService:
    """Factory-Funktion für CarrierService."""
    return CarrierService(repo=repo)


def get_write_service(
    repo: Annotated[CarrierRepository, Depends(get_repository)]
) -> CarrierWriteService:
    """Factory-Funktion für CarrierWriteService."""
    return CarrierWriteService(repo=repo)
