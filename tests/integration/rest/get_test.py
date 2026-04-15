# ruff: noqa: S101, D103

"""Tests für GET mit Query-Parameter."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark

_MIN_PAGES: Final = 2


@mark.rest
@mark.get_request
@mark.parametrize(
    "name",
    ["USS Gerald R. Ford", "JS Izumo"],
)
def test_get_by_name(name: str) -> None:
    # arrange
    params = {"name": name}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) == 1
    carrier = content[0]
    assert carrier is not None
    assert carrier.get("name") == name
    assert carrier.get("id") is not None


@mark.rest
@mark.get_request
@mark.parametrize("name", ["Nicht vorhanden", "Foo-Bar"])
def test_get_by_name_not_found(name: str) -> None:
    # arrange
    params = {"name": name}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) == 0


@mark.rest
@mark.get_request
@mark.parametrize("nation", ["USA", "Japan"])
def test_get_by_nation(nation: str) -> None:
    # arrange
    params = {"nation": nation}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) >= 1
    for carrier in content:
        nation_response = carrier.get("nation")
        assert nation_response is not None and isinstance(nation_response, str)
        assert nation_response == nation
        assert carrier.get("id") is not None


@mark.rest
@mark.get_request
@mark.parametrize("nation", ["Deutschland", "Frankreich"])
def test_get_by_nation_not_found(nation: str) -> None:
    # arrange
    params = {"nation": nation}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) == 0


@mark.rest
@mark.get_request
@mark.parametrize(
    "carrier_type",
    ["AIRCRAFT_CARRIER", "HELICOPTER_CARRIER"],
)
def test_get_by_carrier_type(carrier_type: str) -> None:
    # arrange
    params = {"carrier_type": carrier_type}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) >= 1
    for carrier in content:
        carrier_type_response = carrier.get("carrier_type")
        assert carrier_type_response is not None
        assert carrier_type_response == carrier_type
        assert carrier.get("id") is not None


@mark.rest
@mark.get_request
@mark.parametrize("carrier_type", ["SUBMARINE", "DESTROYER"])
def test_get_by_carrier_type_not_found(carrier_type: str) -> None:
    # arrange
    params = {"carrier_type": carrier_type}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body["content"]
    assert isinstance(content, list)
    assert len(content) == 0


@mark.rest
@mark.get_request
def test_get_page_0() -> None:
    # arrange
    params = {"page": 0, "size": 1}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)

    content: Final = response_body["content"]
    page: Final = response_body["page"]

    assert isinstance(content, list)
    assert len(content) == 1
    assert page["number"] == 0
    assert page["size"] == 1
    assert page["total_elements"] >= _MIN_PAGES
    assert page["total_pages"] >= _MIN_PAGES


@mark.rest
@mark.get_request
def test_get_page_1() -> None:
    # arrange
    params = {"page": 1, "size": 1}
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(rest_url, params=params, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)

    content: Final = response_body["content"]
    page: Final = response_body["page"]

    assert isinstance(content, list)
    assert len(content) == 1
    assert page["number"] == 1
    assert page["size"] == 1
    assert page["total_elements"] >= _MIN_PAGES
    assert page["total_pages"] >= _MIN_PAGES
