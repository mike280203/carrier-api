"""Read-Router für Carrier."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from carrier.problem_details import create_problem_details
from carrier.repository import Session
from carrier.repository.pageable import Pageable
from carrier.repository.slice import Slice
from carrier.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from carrier.router.dependencies import get_service
from carrier.router.page import Page
from carrier.security.role import Role
from carrier.security.roles_required import RolesRequired
from carrier.service.carrier_dto import CarrierDTO
from carrier.service.carrier_service import CarrierService
from carrier.service.exceptions import CarrierNotFoundError

__all__ = ["router"]

router: Final = APIRouter(prefix="/rest/carriers", tags=["Lesen"])


@router.get(
    "/{carrier_id}", dependencies=[Depends(RolesRequired([Role.ADMIN, Role.USER]))]
)
def get_carrier_by_id(
    carrier_id: int,
    request: Request,
    service: Annotated[CarrierService, Depends(get_service)],
) -> Response:
    """Lese einen Carrier anhand seiner ID."""
    logger.debug("carrier_id={}", carrier_id)

    with Session() as session:
        try:
            carrier: Final = service.find_by_id(carrier_id=carrier_id, session=session)
        except CarrierNotFoundError as ex:
            return create_problem_details(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex),
            )

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)
        try:
            if int(version) == carrier.version:
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
        except ValueError:
            logger.debug("ungueltige Version in If-None-Match={}", version)

    return JSONResponse(
        content=_carrier_to_dict(carrier),
        headers={ETAG: f'"{carrier.version}"'},
    )


@router.get("", dependencies=[Depends(RolesRequired([Role.ADMIN, Role.USER]))])
def get_carriers(
    request: Request,
    service: Annotated[CarrierService, Depends(get_service)],
) -> JSONResponse:
    """Lese Carrier mit optionalen Suchparametern."""
    query_params: Final = request.query_params
    logger.debug("{}", query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    suchparameter.pop("page", None)
    suchparameter.pop("size", None)

    with Session() as session:
        carrier_slice: Final = service.find(
            suchparameter=suchparameter,
            pageable=pageable,
            session=session,
        )

    result: Final = _carrier_slice_to_page(carrier_slice, pageable)
    logger.debug("{}", result)
    return JSONResponse(content=result)


def _carrier_slice_to_page(
    carrier_slice: Slice[CarrierDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    carrier_dict = tuple(_carrier_to_dict(carrier) for carrier in carrier_slice.content)
    page: Final = Page.create(
        content=carrier_dict,
        pageable=pageable,
        total_elements=carrier_slice.total_elements,
    )
    return asdict(obj=page)


def _carrier_to_dict(carrier: CarrierDTO) -> dict[str, Any]:
    """Konvertiere CarrierDTO in ein Dict für JSON-Responses."""
    carrier_dict: Final = asdict(obj=carrier)
    carrier_dict.pop("version")
    return carrier_dict
