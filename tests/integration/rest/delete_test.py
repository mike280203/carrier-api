# ruff: noqa: S101, D103
"""Tests für DELETE."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import delete
from pytest import mark


@mark.rest
@mark.delete_request
def test_delete() -> None:
    # arrange
    carrier_id: Final = 1000
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = delete(
        f"{rest_url}/{carrier_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT


@mark.rest
@mark.delete_request
def test_delete_not_found() -> None:
    # arrange
    carrier_id: Final = 999999
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = delete(
        f"{rest_url}/{carrier_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND
