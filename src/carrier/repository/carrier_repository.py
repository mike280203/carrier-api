"""Repository fuer persistente Carrierdaten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from carrier.entity.carrier import Carrier

__all__ = ["CarrierRepository"]


class CarrierRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Carrier."""

    def find_by_id(self, carrier_id: int | None, session: Session) -> Carrier | None:
        """Suche mit der Carrier-ID."""
        logger.debug("carrier_id={}", carrier_id)  # NOSONAR

        if carrier_id is None:
            return None

        statement: Final = (
            select(Carrier).options(joinedload(Carrier.commandcenter))
            .where(Carrier.id == carrier_id)
        )

        carrier: Final = session.scalar(statement)

        logger.debug("{}", carrier)
        return carrier
