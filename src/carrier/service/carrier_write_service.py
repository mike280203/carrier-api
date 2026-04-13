"""Geschäftslogik für schreibende Zugriffe auf Carrier."""

from typing import Final

from loguru import logger
from sqlalchemy.orm import Session

from carrier.repository.carrier_repository import CarrierRepository
from carrier.router.carrier_model import CarrierModel
from carrier.router.carrier_update_model import CarrierUpdateModel
from carrier.service.carrier_dto import CarrierDTO
from carrier.service.exceptions import (
    CarrierNameExistsError,
    CarrierNotFoundError,
    PreconditionFailedError,
)

__all__ = ["CarrierWriteService"]


class CarrierWriteService:
    """Service-Klasse für schreibende Geschäftslogik rund um Carrier."""

    def __init__(self, repo: CarrierRepository) -> None:
        """Initialisierung mit dem zugehörigen Repository."""
        self.repo = repo

    def create(self, carrier_model: CarrierModel, session: Session) -> CarrierDTO:
        """Erzeuge einen neuen Carrier."""
        logger.debug("carrier_model={}", carrier_model)
        if self.repo.exists_name(name=carrier_model.name, session=session):
            raise CarrierNameExistsError(name=carrier_model.name)

        carrier = carrier_model.to_carrier()
        created_carrier = self.repo.create(carrier=carrier, session=session)
        session.commit()
        session.refresh(created_carrier)

        carrier_dto: Final = CarrierDTO(carrier=created_carrier)
        logger.debug("carrier_dto={}", carrier_dto)
        return carrier_dto

    def update(
        self,
        carrier_id: int,
        carrier_update_model: CarrierUpdateModel,
        expected_version: int,
        session: Session,
    ) -> CarrierDTO:
        """Aktualisiere einen vorhandenen Carrier."""
        logger.debug(
            "carrier_id={}, carrier_update_model={}",
            carrier_id,
            carrier_update_model,
        )
        carrier_db = self.repo.find_by_id(carrier_id=carrier_id, session=session)
        if carrier_db is None:
            raise CarrierNotFoundError(carrier_id=carrier_id)

        if expected_version != carrier_db.version:
            raise PreconditionFailedError(
                expected_version=carrier_db.version,
                actual_value=str(expected_version),
            )

        if (
            carrier_update_model.name != carrier_db.name
            and self.repo.exists_name(name=carrier_update_model.name, session=session)
        ):
            raise CarrierNameExistsError(name=carrier_update_model.name)

        carrier = carrier_update_model.to_carrier()
        carrier.id = carrier_id
        if carrier.carrier_type is None:
            carrier.carrier_type = carrier_db.carrier_type

        updated_carrier = self.repo.update(carrier=carrier, session=session)
        if updated_carrier is None:
            raise CarrierNotFoundError(carrier_id=carrier_id)

        session.commit()
        session.refresh(updated_carrier)

        carrier_dto: Final = CarrierDTO(carrier=updated_carrier)
        logger.debug("carrier_dto={}", carrier_dto)
        return carrier_dto

    def delete_by_id(self, carrier_id: int, session: Session) -> None:
        """Lösche einen Carrier anhand seiner ID."""
        logger.debug("carrier_id={}", carrier_id)
        carrier = self.repo.find_by_id(carrier_id=carrier_id, session=session)
        if carrier is None:
            raise CarrierNotFoundError(carrier_id=carrier_id)

        self.repo.delete_by_id(carrier_id=carrier_id, session=session)
        session.commit()
