"""SQLAlchemy-Engine und Session-Factory."""

from typing import Final

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from carrier.config import db_connect_args, db_log_statements, db_url

__all__ = ["Session", "engine"]

engine: Final = create_engine(
    db_url,
    connect_args=db_connect_args,
    echo=db_log_statements,
)

logger.info("Engine fuer SQLAlchemy erzeugt")

Session: Final = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

logger.info("Session-Factory fuer SQLAlchemy erzeugt")
