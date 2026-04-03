"""Entity-Klasse für Carrier."""

from sqlalchemy import Enum, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from carrier.entity.base import Base
from carrier.entity.carrier_type import CarrierType


class Carrier(Base):
    """Entity-Klasse für Carrier."""

    __tablename__ = "carrier"

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )

    name: Mapped[str]
    nation: Mapped[str]
    carrier_type: Mapped[CarrierType] = mapped_column(Enum(CarrierType))

    # 1:1 zu CommandCenter
    command_center: Mapped["CommandCenter"] = relationship(
        back_populates="carrier",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # 1:N zu Aircraft
    aircrafts: Mapped[list["Aircraft"]] = relationship(
        back_populates="carrier",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"Carrier(id={self.id}, name={self.name}, "
            f"nation={self.nation}, carrier_type={self.carrier_type})"
        )
