# ruff: noqa: D103

"""Fixture für pytest: Neuladen der Datenbank."""

from common_test import check_readiness
from pytest import fixture
from sqlalchemy import text

from carrier.config.dev.db_populate import get_db_populate_service
from carrier.repository import engine

session_scope = "session"


@fixture(scope=session_scope, autouse=True)
def check_readiness_per_session() -> None:
    """Prüft einmalig beim Start der Tests, ob der Appserver läuft."""
    check_readiness()
    # Ausgabe in report.html im Wurzelverzeichnis des Projekts
    print("Appserver ist 'ready'")


@fixture(autouse=True)
def reset_database() -> None:

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE carrier RESTART IDENTITY CASCADE;"))

    get_db_populate_service().populate()
