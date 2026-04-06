"""Repository fuer persistente Carrierdaten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from carrier.entity.carrier import Carrier
from carrier.entity.carrier_type import CarrierType
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

    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Carrier]:
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

    def _find_by_name(self, name: str, session: Session) -> Carrier | None:
        logger.debug("name={}", name)
        statement: Final = select(Carrier).options(
            joinedload(Carrier.commandcenter)).where(Carrier.name == name)
        carrier: Final = session.scalar(statement)
        logger.debug("{}", carrier)
        return carrier

    def _find_by_nation(
        self, teil: str, pageable: Pageable,
        session: Session) -> Slice[Carrier]:
        logger.debug("nation={}", teil)
        offset = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = select(Carrier).options(
            joinedload(Carrier.commandcenter)).filter(
                Carrier.nation.ilike(f"%{teil}%")).limit(
                    pageable.size).offset(offset)
        else:
            statement: Final = select(Carrier).options(
            joinedload(Carrier.commandcenter)).filter(
                Carrier.nation.ilike(f"%{teil}%"))

        carriers: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_nation(teil, session)
        carrier_slice: Final = Slice(content=tuple(carriers), total_elements=anzahl)
        logger.debug("{}", carrier_slice)
        return carrier_slice

    def _count_rows_nation(
        self, teil: str, session: Session) -> int:
        statement: Final = select(func.count()).select_from(
            Carrier).filter(Carrier.nation.ilike(f"%{teil}%"))
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_carrier_type(
        self, carrier_type: CarrierType,
         pageable: Pageable, session: Session) -> Slice[Carrier]:
        logger.debug("carrier_type={}", carrier_type)
        offset = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = select(Carrier).options(
            joinedload(Carrier.commandcenter)).filter(
                Carrier.carrier_type == carrier_type).limit(
                    pageable.size).offset(offset)
        else:
            statement: Final = select(Carrier).options(
            joinedload(Carrier.commandcenter)).filter(
                Carrier.carrier_type == carrier_type)

        carriers: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_carrier_type(carrier_type, session)
        carrier_slice: Final = Slice(content=tuple(carriers), total_elements=anzahl)
        logger.debug("{}", carrier_slice)
        return carrier_slice

    def _count_rows_carrier_type(
        self, carrier_type: CarrierType,
        session: Session) -> int:
        statement: Final = select(func.count()).select_from(
            Carrier).filter(Carrier.carrier_type == carrier_type)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0
