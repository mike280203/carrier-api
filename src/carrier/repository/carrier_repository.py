"""Repository fuer persistente Carrierdaten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from carrier.entity.carrier import Carrier
from carrier.repository.pageable import Pageable
from carrier.repository.slice import Slice

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

    def find_all(self, pageable: Pageable, session: Session) -> Slice[Carrier]:
        """Methode zum suchen aller Carrier."""
        logger.debug("aufgerufen")
        offset = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = (
                select(Carrier)
                .options(joinedload(Carrier.commandcenter))
                .limit(pageable.size)
                .offset(offset)
            )
        else:
            statement: Final = select(Carrier).options(
                joinedload(Carrier.commandcenter))

        carriers: Final = session.scalars(statement).all()
        anzahl: Final = self._count_all_rows(session)
        carrier_slice: Final = Slice(content=tuple(carriers), total_elements=anzahl)
        logger.debug("carrier_slice={}", carrier_slice)
        return carrier_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Carrier)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0
