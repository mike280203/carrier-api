"""Pydantic-Model für ein Aircraft."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from carrier.entity import Aircraft

__all__ = ["AircraftModel"]


class AircraftModel(BaseModel):
    """Repräsentiert ein Aircraft-Modell für die API."""

    model: Annotated[str, StringConstraints(
        pattern=r"^[A-Za-z0-9][A-Za-z0-9 .-]{0,49}$")]

    manufacturer: Annotated[str, StringConstraints(
        pattern=r"^[A-Za-z][A-Za-z0-9 .-]{1,49}$")]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "F35",
                "manufacturer": "Lockheed-Martin",
            },
        }
    )

    def to_aircraft(self) -> Aircraft:
        """Konvertierung in ein Aircraft-Objekt für SQLAlchemy."""
        aircraft_dict = self.model_dump()
        aircraft_dict["id"] = None
        aircraft_dict["carrier_id"] = None
        aircraft_dict["carrier"] = None

        return Aircraft(**aircraft_dict)
