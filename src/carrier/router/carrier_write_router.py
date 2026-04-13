"""Write-Router für Carrier."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from carrier.problem_details import create_problem_details
from carrier.repository import Session
from carrier.router.carrier_model import CarrierModel
from carrier.router.carrier_update_model import CarrierUpdateModel
from carrier.router.constants import ETAG, IF_MATCH, IF_MATCH_MIN_LEN
from carrier.router.dependencies import get_write_service
from carrier.service.carrier_write_service import CarrierWriteService
from carrier.service.exceptions import (
    CarrierNameExistsError,
    CarrierNotFoundError,
    PreconditionFailedError,
    PreconditionRequiredError,
)

__all__ = ["router"]

router: Final = APIRouter(prefix="/rest/carriers", tags=["Schreiben"])


@router.post("")
def post(
    carrier_model: CarrierModel,
    request: Request,
    service: Annotated[CarrierWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um einen neuen Carrier anzulegen."""
    logger.debug("carrier_model={}", carrier_model)

    with Session() as session:
        try:
            carrier_dto: Final = service.create(
                carrier_model=carrier_model,
                session=session,
            )
        except CarrierNameExistsError as ex:
            return create_problem_details(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(ex),
            )

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{carrier_dto.id}"},
    )


@router.put("/{carrier_id}")
def put(
    carrier_id: int,
    carrier_update_model: CarrierUpdateModel,
    request: Request,
    service: Annotated[CarrierWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um einen Carrier zu aktualisieren."""
    logger.debug(
        "carrier_id={}, carrier_update_model={}",
        carrier_id,
        carrier_update_model,
    )

    try:
        expected_version: Final = _extract_if_match_version(request)
    except PreconditionRequiredError as ex:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail=str(ex),
        )
    except PreconditionFailedError as ex:
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=str(ex),
        )

    with Session() as session:
        try:
            carrier_modified: Final = service.update(
                carrier_id=carrier_id,
                carrier_update_model=carrier_update_model,
                expected_version=expected_version,
                session=session,
            )
        except CarrierNotFoundError as ex:
            return create_problem_details(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex),
            )
        except CarrierNameExistsError as ex:
            return create_problem_details(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(ex),
            )
        except PreconditionFailedError as ex:
            return create_problem_details(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail=str(ex),
            )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={ETAG: f'"{carrier_modified.version}"'},
    )


@router.delete("/{carrier_id}")
def delete_by_id(
    carrier_id: int,
    service: Annotated[CarrierWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um einen Carrier anhand seiner ID zu löschen."""
    logger.debug("carrier_id={}", carrier_id)

    with Session() as session:
        try:
            service.delete_by_id(carrier_id=carrier_id, session=session)
        except CarrierNotFoundError as ex:
            return create_problem_details(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex),
            )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _extract_if_match_version(request: Request) -> int:
    """Lese und validiere die Version aus dem If-Match-Header."""
    if_match_value: Final = request.headers.get(IF_MATCH)

    if if_match_value is None:
        raise PreconditionRequiredError

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        raise PreconditionFailedError(
            expected_version=-1,
            actual_value=if_match_value,
        )

    version: Final = if_match_value[1:-1]
    try:
        return int(version)
    except ValueError as ex:
        raise PreconditionFailedError(
            expected_version=-1,
            actual_value=if_match_value,
        ) from ex
