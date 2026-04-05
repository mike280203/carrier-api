"""Entity-Klasse für Carrier."""

from datetime import datetime
from typing import Any, Self

from sqlalchemy import Enum, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from carrier.entity.base import Base
from carrier.entity.carrier_type import CarrierType


class Carrier(Base):
    """Entity-Klasse für Carrier."""

    __tablename__ = "carrier"

    name: Mapped[str]
    """Der Name des Carriers."""

    nation: Mapped[str]
    """Die Nation des Carriers."""

    carrier_type: Mapped[CarrierType] = mapped_column(Enum(CarrierType))
    """Der Typ des Carriers."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    commandcenter: Mapped[CommandCenter] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable ]
        back_populates="carrier",
        uselist=False,
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Das in einer 1:1-Beziehung referenzierte CommandCenter."""

    aircrafts: Mapped[list[Aircraft]] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable ]
        back_populates="carrier",
        cascade="save-update, delete",
    )
    """Die in einer 1:N-Beziehung referenzierten Aircrafts."""

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Die Versionsnummer für optimistische Synchronisation."""

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
    """Der Zeitstempel für das initiale INSERT in die DB-Tabelle."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )
    """Der Zeitstempel des letzten UPDATEs in der DB-Tabelle."""

    __mapper_args__ = {"version_id_col": version}

    def set(self, carrier: Self) -> None:
        """Primitive Attributwerte überschreiben, z. B. vor DB-Update."""
        self.name = carrier.name
        self.nation = carrier.nation
        self.carrier_type = carrier.carrier_type

    def __eq__(self, other: Any) -> bool:
        """Vergleich auf Gleichheit, ohne Joins zu verursachen."""
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Funktion anhand der ID, ohne Joins zu verursachen."""
        return hash(self.id) if self.id is not None else hash(type(self))

    def __repr__(self) -> str:
        """Ausgabe eines Carriers als String, ohne Joins zu verursachen."""
        return (
            f"Carrier(id={self.id}, version={self.version}, "
            f"name={self.name}, nation={self.nation}, "
            f"carrier_type={self.carrier_type}, "
            f"erzeugt={self.erzeugt}, aktualisiert={self.aktualisiert})"
        )
