"""Schema für GraphQL durch Strawberry."""

from collections.abc import Sequence
from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter

from carrier.config.graphql import graphql_ide
from carrier.graphql_api.graphql_types import (
    CarrierInput,
    CreatePayload,
    Suchparameter,
)
from carrier.repository import Session
from carrier.repository.carrier_repository import CarrierRepository
from carrier.repository.pageable import Pageable
from carrier.router.carrier_model import CarrierModel
from carrier.service.carrier_dto import CarrierDTO
from carrier.service.carrier_service import CarrierService
from carrier.service.carrier_write_service import CarrierWriteService
from carrier.service.exceptions import CarrierNotFoundError

__all__ = ["Mutation", "Query", "graphql_router"]


_repo: Final = CarrierRepository()
_service: Final = CarrierService(_repo)
_write_service: Final = CarrierWriteService(_repo)


@strawberry.type
class Query:
    """Query, um Carrierdaten zu lesen."""

    @strawberry.field
    def carrier(self, carrier_id: strawberry.ID) -> CarrierDTO | None:
        """Daten zu einem Carrier lesen."""
        logger.debug("carrier_id={}", carrier_id)

        with Session() as session:
            try:
                carrier_dto: Final = _service.find_by_id(
                    carrier_id=int(carrier_id),
                    session=session,
                )
            except CarrierNotFoundError:
                return None

        logger.debug("carrier_dto={}", carrier_dto)
        return carrier_dto

    @strawberry.field
    def carriers(self, suchparameter: Suchparameter | None = None) -> Sequence[CarrierDTO]:  # noqa: E501
        """Carrier anhand optionaler Suchparameter suchen."""
        logger.debug("suchparameter={}", suchparameter)

        if suchparameter is None:
            suchparameter_filtered: dict[str, str] = {}
        else:
            suchparameter_dict = dict(vars(suchparameter))
            suchparameter_filtered = {
                key: value.value if hasattr(value, "value") else value
                for key, value in suchparameter_dict.items()
                if value is not None and value
            }

        logger.debug("suchparameter_filtered={}", suchparameter_filtered)

        pageable: Final = Pageable.create(size=str(0))

        with Session() as session:
            carrier_slice = _service.find(
                suchparameter=suchparameter_filtered,
                pageable=pageable,
                session=session,
            )

        logger.debug("carrier_slice={}", carrier_slice)
        return carrier_slice.content


@strawberry.type
class Mutation:
    """Mutations, um Carrierdaten anzulegen."""

    @strawberry.mutation
    def create(self, carrier_input: CarrierInput) -> CreatePayload:
        """Einen neuen Carrier anlegen."""
        logger.debug("carrier_input={}", carrier_input)

        carrier_dict = carrier_input.__dict__.copy()
        carrier_dict["commandcenter"] = carrier_input.commandcenter.__dict__
        carrier_dict["aircrafts"] = [
            aircraft.__dict__ for aircraft in carrier_input.aircrafts
        ]

        carrier_model: Final = CarrierModel.model_validate(carrier_dict)

        with Session() as session:
            carrier_dto: Final = _write_service.create(
                carrier_model=carrier_model,
                session=session,
            )

        payload: Final = CreatePayload(id=carrier_dto.id)
        logger.debug("payload={}", payload)
        return payload


schema: Final = strawberry.Schema(query=Query, mutation=Mutation)

Context = dict[str, Request]


def get_context(request: Request) -> Context:
    """Request von FastAPI an Strawberry weiterreichen."""
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema,
    context_getter=get_context,
    graphql_ide=graphql_ide,
)
