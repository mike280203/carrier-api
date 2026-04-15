# ruff: noqa: S101, D103

"""Tests für POST."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, login, rest_url
from httpx import post
from pytest import mark


@mark.rest
@mark.post_request
def test_post() -> None:
    # arrange
    neuer_carrier: Final = {
        "name": "Test Carrier REST",
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "RestCC",
            "security_level": 4,
        },
        "aircrafts": [
            {
                "model": "F-35C",
                "manufacturer": "Lockheed Martin",
            },
            {
                "model": "E-2D Hawkeye",
                "manufacturer": "Northrop Grumman",
            },
        ],
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # act
    response: Final = post(
        rest_url,
        json=neuer_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neuer_carrier_invalid: Final = {
        "name": "",
        "nation": "",
        "carrier_type": "SUBMARINE",
        "commandcenter": {
            "code_name": "",
            "security_level": 99,
        },
        "aircrafts": [
            {
                "model": "",
                "manufacturer": "",
            },
        ],
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # act
    response: Final = post(
        rest_url,
        json=neuer_carrier_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@mark.rest
@mark.post_request
def test_post_name_exists() -> None:
    # arrange
    name_exists: Final = "USS Gerald R. Ford"
    neuer_carrier: Final = {
        "name": name_exists,
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "DuplicateCC",
            "security_level": 3,
        },
        "aircrafts": [
            {
                "model": "FA-18E Super Hornet",
                "manufacturer": "Boeing",
            },
        ],
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # act
    response: Final = post(
        rest_url,
        json=neuer_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CONFLICT
    assert name_exists in response.text


@mark.rest
@mark.post_request
def test_post_invalid_json() -> None:
    # arrange
    json_invalid: Final = '{"name" "Carrier"}'
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # act
    response: Final = post(
        rest_url,
        content=json_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "JSON decode error" in response.text
