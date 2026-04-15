# ruff: noqa: S101, D103

"""Tests für den Health-Endpunkt."""

from http import HTTPStatus
from typing import Any, Final

from common_test import ctx, health_url, timeout
from httpx import get
from pytest import mark


@mark.rest
@mark.health
def test_health() -> None:
    response: Final = get(health_url, verify=ctx, timeout=timeout)

    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)

    status_value: Final[Any | None] = response_body.get("status")
    assert status_value == "ok"
