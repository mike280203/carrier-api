"""SQLAlchemy-Engine und Session-Factory."""

from typing import Final

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from carrier.config import db_connect_args, db_log_statements, db_url

engine: Final = create_engine(
    db_url,
    connect_args=db_connect_args,
    echo=db_log_statements,
)

SessionLocal: Final = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
