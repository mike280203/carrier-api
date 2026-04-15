# ruff: noqa: D103

"""Fixture für pytest: Neuladen der Datenbank."""

from common_test import check_readiness
from pytest import fixture

session_scope = "session"


@fixture(scope=session_scope, autouse=True)
def check_readiness_per_session() -> None:
    check_readiness()
    # Ausgabe in report.html im Wurzelverzeichnis des Projekts
    print("Appserver ist 'ready'")
