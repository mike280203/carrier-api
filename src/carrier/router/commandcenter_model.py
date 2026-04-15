"""Pydantic-Model für ein CommandCenter."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from carrier.entity import CommandCenter

__all__ = ["CommandCenterModel"]


class CommandCenterModel(BaseModel):
    """Repräsentiert ein CommandCenter-Modell für die API."""

    code_name: Annotated[
        str, StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9 .-]{1,49}$")
    ]

    security_level: Annotated[int, Field(ge=1, le=99)]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code_name": "Pentagon",
                "security_level": 3,
            },
        }
    )

    def to_commandcenter(self) -> CommandCenter:
        """Konvertierung in ein CommandCenter-Objekt für SQLAlchemy."""
        commandcenter_dict = self.model_dump()

        return CommandCenter(**commandcenter_dict)
