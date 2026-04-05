"""Basisklasse für Entity-Klassen."""

from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:

    class MappedAsDataclass:
        """Mixin-Klasse, ohne die Directiven von PEP 681 zu verwenden."""

        def __init__(self, *arg: Any, **kw: Any) -> None:
            """Mixin-Klasse, ohne die Directiven von PEP 681 zu verwenden."""

else:
    from sqlalchemy.orm import MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Basisklasse für Entity-Klassen als Dataclass."""
