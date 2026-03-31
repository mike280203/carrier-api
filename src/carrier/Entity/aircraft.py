"""Entity-Klasse für Aircraft."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from carrier.entity.base import Base


class Aircraft(Base):
    """Entity-Klasse für Aircraft."""

    __tablename__ = "aircraft"

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )

    model: Mapped[str]
    manufacturer: Mapped[str]

    carrier_id: Mapped[int] = mapped_column(ForeignKey("carrier.id"))

    carrier: Mapped["Carrier"] = relationship(
        back_populates="aircrafts",
    )

    def __repr__(self) -> str:
        return (
            f"Aircraft(id={self.id}, model={self.model}, "
            f"manufacturer={self.manufacturer})"
        )