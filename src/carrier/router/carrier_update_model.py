"""Pydantic-Model zum Aktualisieren eines Carriers."""

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, StringConstraints

from carrier.entity.carrier import Carrier
from carrier.entity.carrier_type import CarrierType

__all__ = ["CarrierUpdateModel"]


class CarrierUpdateModel(BaseModel):
    """Pydantic-Model zum Aktualisieren von Carrier."""

    name: Annotated[str, StringConstraints(
        pattern=r"^[A-Za-z0-9][A-Za-z0-9 .'-]{1,49}$")]

    nation: Annotated[str, StringConstraints(
        pattern=r"^[A-Za-z][A-Za-z .'-]{1,49}$")]

    carrier_type: CarrierType | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Pentagon",
                "nation": "United States",
                "carrier_type": "AIRCRAFT_CARRIER"
            },
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Konvertierung der primitiven Attribute in ein Dictionary."""
        carrier_dict = self.model_dump()
        carrier_dict["id"] = None
        carrier_dict["aircrafts"] = []
        carrier_dict["commandcenter"] = None

        return carrier_dict

    def to_carrier(self) -> Carrier:
        """Konvertierung in ein Carrier-Objekt für SQLAlchemy."""
        carrier_dict = self.to_dict()

        carrier = Carrier(**carrier_dict)
        return carrier  # noqa: RET504
