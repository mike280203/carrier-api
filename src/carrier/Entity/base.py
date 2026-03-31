"""Basisklasse für Entity-Klassen."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Basisklasse für alle Entities."""