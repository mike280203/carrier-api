# ruff: noqa: S101, D103

"""Tests für PUT."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get, put
from pytest import mark

NAME_UPDATE: Final = "USS Enterprise Updated"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    carrier_id: Final = 1000
    token: Final = login()
    assert token is not None

    get_response = get(
        f"{rest_url}/{carrier_id}",
        headers={"Authorization": f"Bearer {token}"},
        verify=ctx
    )

    aktuelles_etag = get_response.headers.get("ETag", '"0"')

    geaenderter_carrier: Final = {
        "name": NAME_UPDATE,
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "UpdatedCC",
            "security_level": 5,
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

    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": aktuelles_etag,
    }

    # act
    response: Final = put(
        f"{rest_url}/{carrier_id}",
        json=geaenderter_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT


@mark.rest
@mark.put_request
def test_put_invalid() -> None:
    # arrange
    carrier_id: Final = 1000
    geaenderter_carrier_invalid: Final = {
        "name": "",
        "nation": "",
        "carrier_type": "SUBMARINE",
        "commandcenter": {
            "code_name": "",
            "security_level": 999,
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
        "If-Match": '"0"',
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{carrier_id}",
        json=geaenderter_carrier_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "name" in response.text
    assert "nation" in response.text
    assert "carrier_type" in response.text


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    carrier_id: Final = 999999
    if_match: Final = '"0"'
    geaenderter_carrier: Final = {
        "name": NAME_UPDATE,
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "UpdatedCC",
            "security_level": 5,
        },
        "aircrafts": [
            {
                "model": "F-35C",
                "manufacturer": "Lockheed Martin",
            },
        ],
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{carrier_id}",
        json=geaenderter_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_name_exists() -> None:
    # arrange
    carrier_id: Final = 1001
    token: Final = login()
    assert token is not None

    get_response = get(
        f"{rest_url}/{carrier_id}",
        headers={"Authorization": f"Bearer {token}"},
        verify=ctx,
    )
    aktuelles_etag = get_response.headers.get("ETag", '"0"')

    name_exists: Final = "USS Enterprise Updated"

    geaenderter_carrier: Final = {
        "name": name_exists,
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "UpdatedCC",
            "security_level": 5,
        },
        "aircrafts": [
            {
                "model": "F-35C",
                "manufacturer": "Lockheed Martin",
            },
        ],
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": aktuelles_etag,
    }

    # act
    response: Final = put(
        f"{rest_url}/{carrier_id}",
        json=geaenderter_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code in {
        HTTPStatus.CONFLICT,
        HTTPStatus.UNPROCESSABLE_ENTITY,
    }
    assert name_exists in response.text


@mark.rest
@mark.put_request
def test_put_ohne_versionsnr() -> None:
    # arrange
    carrier_id: Final = 1000
    geaenderter_carrier: Final = {
        "name": NAME_UPDATE,
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "UpdatedCC",
            "security_level": 5,
        },
        "aircrafts": [
            {
                "model": "F-35C",
                "manufacturer": "Lockheed Martin",
            },
        ],
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{carrier_id}",
        json=geaenderter_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_REQUIRED


@mark.rest
@mark.put_request
def test_put_alte_versionsnr() -> None:
    # arrange
    carrier_id: Final = 1000
    if_match: Final = '"-1"'
    geaenderter_carrier: Final = {
        "name": NAME_UPDATE,
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "UpdatedCC",
            "security_level": 5,
        },
        "aircrafts": [
            {
                "model": "F-35C",
                "manufacturer": "Lockheed Martin",
            },
        ],
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{carrier_id}",
        json=geaenderter_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED


@mark.rest
@mark.put_request
def test_put_ungueltige_versionsnr() -> None:
    # arrange
    carrier_id: Final = 1000
    if_match: Final = '"xy"'
    geaenderter_carrier: Final = {
        "name": NAME_UPDATE,
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "UpdatedCC",
            "security_level": 5,
        },
        "aircrafts": [
            {
                "model": "F-35C",
                "manufacturer": "Lockheed Martin",
            },
        ],
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{carrier_id}",
        json=geaenderter_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED


@mark.rest
@mark.put_request
def test_put_versionsnr_ohne_quotes() -> None:
    # arrange
    carrier_id: Final = 1000
    if_match: Final = "0"
    geaenderter_carrier: Final = {
        "name": NAME_UPDATE,
        "nation": "USA",
        "carrier_type": "AIRCRAFT_CARRIER",
        "commandcenter": {
            "code_name": "UpdatedCC",
            "security_level": 5,
        },
        "aircrafts": [
            {
                "model": "F-35C",
                "manufacturer": "Lockheed Martin",
            },
        ],
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{carrier_id}",
        json=geaenderter_carrier,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
