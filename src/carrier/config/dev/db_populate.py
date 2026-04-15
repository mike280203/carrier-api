"""Neuladen der DB im Modus DEV."""

from loguru import logger
from sqlalchemy import select

from carrier.config.dev_modus import dev_db_populate
from carrier.entity import Aircraft, Carrier, CarrierType, CommandCenter
from carrier.repository import Session, engine

__all__ = ["DbPopulateService", "db_populate", "get_db_populate_service"]


class DbPopulateService:
    """Erzeugt eine minimale, konsistente Entwicklungsdatenbasis."""

    def populate(self) -> None:
        """Tabellen neu anlegen und Beispieldaten einspielen."""
        logger.warning(">>> Die Carrier-DB wird neu aufgebaut: {} <<<", engine.url)

        with Session() as session:
            exists = session.scalar(select(Carrier.id).limit(1))
            if exists is not None:
                logger.debug("Beispieldaten bereits vorhanden")
                return

            carriers = [
                Carrier(
                    name="USS Gerald R. Ford",
                    nation="USA",
                    carrier_type=CarrierType.AIRCRAFT_CARRIER,
                    commandcenter=CommandCenter(
                        code_name="Atlas",
                        security_level=5,
                    ),
                    aircrafts=[
                        Aircraft(
                            model="F/A-18E Super Hornet",
                            manufacturer="Boeing",
                        ),
                        Aircraft(
                            model="E-2D Advanced Hawkeye",
                            manufacturer="Northrop Grumman",
                        ),
                    ],
                ),
                Carrier(
                    name="JS Izumo",
                    nation="Japan",
                    carrier_type=CarrierType.HELICOPTER_CARRIER,
                    commandcenter=CommandCenter(
                        code_name="Shogun",
                        security_level=4,
                    ),
                    aircrafts=[
                        Aircraft(
                            model="SH-60K Seahawk",
                            manufacturer="Mitsubishi",
                        ),
                    ],
                ),
            ]
            session.add_all(carriers)
            session.commit()

        logger.warning(">>> Die Carrier-DB wurde mit Beispieldaten geladen <<<")


def get_db_populate_service() -> DbPopulateService:
    """Factory-Funktion fuer DbPopulateService."""
    return DbPopulateService()


def db_populate() -> None:
    """DB mit Testdaten neu laden, falls im dev-Modus."""
    if dev_db_populate:
        get_db_populate_service().populate()
