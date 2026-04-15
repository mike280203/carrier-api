"""Pydantic-Model für ein Carrier."""

from typing import Final

from loguru import logger

from carrier.entity import Carrier, CarrierType
from carrier.router.aircraft_model import AircraftModel
from carrier.router.carrier_update_model import CarrierUpdateModel
from carrier.router.commandcenter_model import CommandCenterModel

__all__ = ["CarrierModel"]


class CarrierModel(CarrierUpdateModel):
    """Pydantic-Model für die Carrierdaten."""

    commandcenter: CommandCenterModel
    """Der zugehörige CommandCenter."""
    aircrafts: list[AircraftModel]
    """Die Liste der Aircrafts."""
    carrier_type: CarrierType
    """Der Carrier-Typ als Enum-Werte."""

    def to_carrier(self) -> Carrier:
        """Konvertierung in ein Carrier-Objekt für SQLAlchemy."""
        logger.debug("self={}", self)
        carrier_dict = self.to_dict()
        carrier_dict.pop("id", None)
        carrier_dict["carrier_type"] = self.carrier_type

        carrier: Final = Carrier(**carrier_dict)
        carrier.commandcenter = self.commandcenter.to_commandcenter()
        carrier.aircrafts = [
            aircraft_model.to_aircraft() for aircraft_model in self.aircrafts
        ]
        logger.debug("carrier={}", carrier)
        return carrier
