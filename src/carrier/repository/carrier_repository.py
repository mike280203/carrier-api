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
        #todo
