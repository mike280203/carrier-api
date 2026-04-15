"""Entity-Klasse für Aircraft."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from carrier.entity.base import Base


class Aircraft(Base):
    """Entity-Klasse für Aircraft."""

    __tablename__ = "aircraft"

    model: Mapped[str]
    """Das Modell des Aircraft."""

    manufacturer: Mapped[str]
    """Der Hersteller des Aircraft."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
        init=False,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    carrier_id: Mapped[int] = mapped_column(ForeignKey("carrier.id"), init=False)
    """ID des zugehörigen Carriers als Fremdschlüssel in der DB-Tabelle."""

    carrier: Mapped[Carrier] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable ]
        back_populates="aircrafts",
        init=False,
    )
    """Das zugehörige transiente Carrier-Objekt."""

    def __repr__(self) -> str:
        """Ausgabe eines Aircraft als String ohne Carrierdaten."""
        return (
            f"Aircraft(id={self.id}, model={self.model}, "
            f"manufacturer={self.manufacturer})"
        )
