"""Repository fuer persistente Carrierdaten."""

from collections.abc import Mapping
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
            select(Carrier)
            .options(joinedload(Carrier.commandcenter))
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
                joinedload(Carrier.commandcenter)
            )

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
        statement: Final = (
            select(Carrier)
            .options(joinedload(Carrier.commandcenter))
            .where(Carrier.name == name)
        )
        carrier: Final = session.scalar(statement)
        logger.debug("{}", carrier)
        return carrier

    def _find_by_nation(
        self, teil: str, pageable: Pageable, session: Session
    ) -> Slice[Carrier]:
        logger.debug("nation={}", teil)
        offset = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = (
                select(Carrier)
                .options(joinedload(Carrier.commandcenter))
                .filter(Carrier.nation.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(offset)
            )
        else:
            statement: Final = (
                select(Carrier)
                .options(joinedload(Carrier.commandcenter))
                .filter(Carrier.nation.ilike(f"%{teil}%"))
            )

        carriers: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_nation(teil, session)
        carrier_slice: Final = Slice(content=tuple(carriers), total_elements=anzahl)
        logger.debug("{}", carrier_slice)
        return carrier_slice

    def _count_rows_nation(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Carrier)
            .filter(Carrier.nation.ilike(f"%{teil}%"))
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_carrier_type(
        self, carrier_type: CarrierType, pageable: Pageable, session: Session
    ) -> Slice[Carrier]:
        logger.debug("carrier_type={}", carrier_type)
        offset = pageable.number * pageable.size

        if pageable.size != 0:
            statement: Final = (
                select(Carrier)
                .options(joinedload(Carrier.commandcenter))
                .filter(Carrier.carrier_type == carrier_type)
                .limit(pageable.size)
                .offset(offset)
            )
        else:
            statement: Final = (
                select(Carrier)
                .options(joinedload(Carrier.commandcenter))
                .filter(Carrier.carrier_type == carrier_type)
            )

        carriers: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_carrier_type(carrier_type, session)
        carrier_slice: Final = Slice(content=tuple(carriers), total_elements=anzahl)
        logger.debug("{}", carrier_slice)
        return carrier_slice

    def _count_rows_carrier_type(
        self, carrier_type: CarrierType, session: Session
    ) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Carrier)
            .filter(Carrier.carrier_type == carrier_type)
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def exists_name(self, name: str, session: Session) -> bool:
        """Gibt es einen Carrier mit dem namen schon."""
        logger.debug("name={}", name)
        statement: Final = select(func.count()).where(Carrier.name == name)
        anzahl: Final = session.scalar(statement)
        logger.debug("anzahl={}", anzahl)
        return anzahl is not None and anzahl > 0

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[Carrier]:
        """Suche mit Suchparameter."""
        log_str: Final = "{}"
        logger.debug(log_str, suchparameter)
        if not suchparameter:
            return self._find_all(pageable=pageable, session=session)

        # Iteration ueber die Schluessel des Dictionaries mit den Suchparameter
        for key, value in suchparameter.items():
            if key == "name":
                carrier = self._find_by_name(name=value, session=session)
                logger.debug(log_str, carrier)
                return (
                    Slice(content=(carrier,), total_elements=1)
                    if carrier is not None
                    else Slice(content=(), total_elements=0)
                )
            if key == "nation":
                carriers = self._find_by_nation(
                    teil=value, pageable=pageable, session=session
                )
                logger.debug(log_str, carriers)
                return carriers
            if key == "carrier_type":
                try:
                    carrier_type_enum = CarrierType(value)
                except ValueError:
                    return Slice(content=(), total_elements=0)

                carriers = self._find_by_carrier_type(
                    carrier_type_enum, pageable=pageable, session=session
                )
                logger.debug(log_str, carriers)
                return carriers
        return Slice(content=(), total_elements=0)

    def create(self, carrier: Carrier, session: Session) -> Carrier:
        """Speichere einen neuen Carrier ab."""
        logger.debug(
            "carrier={}, carrier.commandcenter={}, carrier.aircrafts={}",
            carrier,
            carrier.commandcenter,
            carrier.aircrafts,
        )
        session.add(instance=carrier)
        session.flush(objects=[carrier])
        logger.debug("carrier_id={}", carrier.id)
        return carrier

    def update(self, carrier: Carrier, session: Session) -> Carrier | None:
        """Aktualisiere einen Carrier."""
        logger.debug("{}", carrier)

        if (
            carrier_db := self.find_by_id(carrier_id=carrier.id, session=session)
        ) is None:
            return None
        carrier_db.set(carrier)

        logger.debug("{}", carrier_db)
        return carrier_db

    def delete_by_id(self, carrier_id: int, session: Session) -> None:
        """Lösche die Daten zu einem Carrier."""
        logger.debug("carrier_id={}", carrier_id)

        if (carrier := self.find_by_id(carrier_id=carrier_id, session=session)) is None:
            return
        session.delete(carrier)
        logger.debug("ok")
