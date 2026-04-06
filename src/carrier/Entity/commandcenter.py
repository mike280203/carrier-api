"""Entity-Klasse für CommandCenter."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from carrier.entity.base import Base


class CommandCenter(Base):
    """Entity-Klasse für CommandCenter."""

    __tablename__ = "command_center"

    code_name: Mapped[str]
    """Der Codename des CommandCenters."""

    security_level: Mapped[int]
    """Die Sicherheitsstufe des CommandCenters."""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    carrier_id: Mapped[int] = mapped_column(
        ForeignKey("carrier.id"),
        unique=True,
    )
    """ID des zugehörigen Carriers als Fremdschlüssel in der DB-Tabelle."""

    carrier: Mapped[Carrier] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
        back_populates="commandcenter",
    )
    """Das zugehörige transiente Carrier-Objekt."""

    def __repr__(self) -> str:
        """Ausgabe eines CommandCenters als String ohne Carrierdaten."""
        return (
            f"CommandCenter(id={self.id}, code_name={self.code_name}, "
            f"security_level={self.security_level})"
        )
