# ruff: noqa: S101, D103

"""Tests für GET mit Pfadparameter für die ID."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, password_user, rest_url, username_user
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
def test_get_by_id_admin() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    response_all: Final = get(
        rest_url,
        headers=headers,
        verify=ctx,
    )
    assert response_all.status_code == HTTPStatus.OK
    response_all_body: Final = response_all.json()
    assert isinstance(response_all_body, dict)

    content: Final = response_all_body.get("content")
    assert isinstance(content, list)
    assert len(content) > 0

    carrier_id: Final = content[0].get("id")
    assert carrier_id is not None

    # act
    response: Final = get(
        f"{rest_url}/{carrier_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == carrier_id


@mark.rest
@mark.get_request
@mark.parametrize("carrier_id", [0, 999999])
def test_get_by_id_not_found(carrier_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{carrier_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_by_id_carrier() -> None:
    # arrange
    admin_token: Final = login()
    assert admin_token is not None
    admin_headers: Final = {"Authorization": f"Bearer {admin_token}"}

    response_all: Final = get(
        rest_url,
        headers=admin_headers,
        verify=ctx,
    )
    assert response_all.status_code == HTTPStatus.OK
    response_all_body: Final = response_all.json()
    assert isinstance(response_all_body, dict)

    content: Final = response_all_body.get("content")
    assert isinstance(content, list)
    assert len(content) > 0

    carrier_id: Final = content[0].get("id")
    assert carrier_id is not None

    token: Final = login(username=username_user, password=password_user)
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{carrier_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    carrier_id_response: Final = response_body.get("id")
    assert carrier_id_response is not None
    assert carrier_id_response == carrier_id


@mark.rest
@mark.get_request
def test_get_by_id_ungueltiger_token() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"{token}XXX"}

    response_all: Final = get(
        rest_url,
        headers={"Authorization": f"Bearer {token}"},
        verify=ctx,
    )
    assert response_all.status_code == HTTPStatus.OK
    response_all_body: Final = response_all.json()
    assert isinstance(response_all_body, dict)

    content: Final = response_all_body.get("content")
    assert isinstance(content, list)
    assert len(content) > 0

    carrier_id: Final = content[0].get("id")
    assert carrier_id is not None

    # act
    response: Final = get(
        f"{rest_url}/{carrier_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.get_request
def test_get_by_id_ohne_token() -> None:
    token: Final = login()
    assert token is not None

    response_all: Final = get(
        rest_url,
        headers={"Authorization": f"Bearer {token}"},
        verify=ctx,
    )
    assert response_all.status_code == HTTPStatus.OK
    response_all_body: Final = response_all.json()
    assert isinstance(response_all_body, dict)

    content: Final = response_all_body.get("content")
    assert isinstance(content, list)
    assert len(content) > 0

    carrier_id: Final = content[0].get("id")
    assert carrier_id is not None

    # act
    response: Final = get(
        f"{rest_url}/{carrier_id}",
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.get_request
def test_get_by_id_etag() -> None:
    # arrange
    token: Final = login()
    assert token is not None

    response_all: Final = get(
        rest_url,
        headers={"Authorization": f"Bearer {token}"},
        verify=ctx,
    )
    assert response_all.status_code == HTTPStatus.OK
    response_all_body: Final = response_all.json()
    assert isinstance(response_all_body, dict)

    content: Final = response_all_body.get("content")
    assert isinstance(content, list)
    assert len(content) > 0

    carrier_id: Final = content[0].get("id")
    assert carrier_id is not None

    headers_first = {"Authorization": f"Bearer {token}"}
    response_first: Final = get(
        f"{rest_url}/{carrier_id}",
        headers=headers_first,
        verify=ctx,
    )
    assert response_first.status_code == HTTPStatus.OK

    etag: Final = response_first.headers.get("ETag")
    assert etag is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "If-None-Match": etag,
    }

    # act
    response: Final = get(
        f"{rest_url}/{carrier_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_MODIFIED
    assert not response.text


@mark.rest
@mark.get_request
@mark.parametrize("if_none_match", ['xxx"', "xxx"])
def test_get_by_id_etag_invalid(if_none_match: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None

    response_all: Final = get(
        rest_url,
        headers={"Authorization": f"Bearer {token}"},
        verify=ctx,
    )
    assert response_all.status_code == HTTPStatus.OK
    response_all_body: Final = response_all.json()
    assert isinstance(response_all_body, dict)

    content: Final = response_all_body.get("content")
    assert isinstance(content, list)
    assert len(content) > 0

    carrier_id: Final = content[0].get("id")
    assert carrier_id is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "If-None-Match": if_none_match,
    }

    # act
    response: Final = get(
        f"{rest_url}/{carrier_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == carrier_id
