"""Entity-Klasse für CommandCenter."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from carrier.entity.base import Base


class CommandCenter(Base):
    """Entity-Klasse für CommandCenter."""

    __tablename__ = "command_center"

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )

    code_name: Mapped[str]
    security_level: Mapped[int]

    carrier_id: Mapped[int] = mapped_column(
        ForeignKey("carrier.id"),
        unique=True,
    )

    carrier: Mapped["Carrier"] = relationship(
        back_populates="command_center",
    )

    def __repr__(self) -> str:
        return (
            f"CommandCenter(id={self.id}, code_name={self.code_name}, "
            f"security_level={self.security_level})"
        )