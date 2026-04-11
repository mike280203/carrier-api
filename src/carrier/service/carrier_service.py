"""Geschäftslogik für lesende Zugriffe auf Carrier."""

from collections.abc import Mapping
from typing import Final

from loguru import logger
from sqlalchemy.orm import Session

from carrier.repository.carrier_repository import CarrierRepository
from carrier.repository.pageable import Pageable
from carrier.repository.slice import Slice
from carrier.service.carrier_dto import CarrierDTO
from carrier.service.exceptions import CarrierNotFoundError

__all__ = ["CarrierService"]


class CarrierService:
    """Service-Klasse für lesende Geschäftslogik rund um Carrier."""

    def __init__(self, repo: CarrierRepository) -> None:
        """Initialisierung mit dem zugehörigen Repository."""
        self.repo = repo

    def find_by_id(self, carrier_id: int, session: Session) -> CarrierDTO:
        """Suche einen Carrier anhand seiner ID."""
        logger.debug("carrier_id={}", carrier_id)
        carrier = self.repo.find_by_id(carrier_id=carrier_id, session=session)
        if carrier is None:
            raise CarrierNotFoundError(carrier_id=carrier_id)

        carrier_dto: Final = CarrierDTO(carrier=carrier)
        logger.debug("carrier_dto={}", carrier_dto)
        return carrier_dto

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[CarrierDTO]:
        """Suche Carrier anhand optionaler Suchparameter."""
        logger.debug("suchparameter={}, pageable={}", suchparameter, pageable)
        carrier_slice = self.repo.find(
            suchparameter=suchparameter,
            pageable=pageable,
            session=session,
        )
        carrier_dtos: Final = tuple(
            CarrierDTO(carrier=carrier) for carrier in carrier_slice.content
        )
        result: Final = Slice(
            content=carrier_dtos,
            total_elements=carrier_slice.total_elements,
        )
        logger.debug("carrier_slice_dto={}", result)
        return result

    # find_by_name,nation,carrier_type noch hinzufügen später
