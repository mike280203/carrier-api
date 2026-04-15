# ruff: noqa: S101, D103

"""Tests für Mutations mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login
from httpx import post
from pytest import mark


@mark.graphql
@mark.mutation
def test_create() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            mutation {
                create(
                    carrierInput: {
                        name: "Carrier GraphQL"
                        nation: "USA"
                        carrierType: AIRCRAFT_CARRIER
                        commandcenter: {
                            codeName: "GraphQLCC"
                            securityLevel: 4
                        }
                        aircrafts: [
                            {
                                model: "F-35C"
                                manufacturer: "Lockheed Martin"
                            }
                            {
                                model: "E-2D Hawkeye"
                                manufacturer: "Northrop Grumman"
                            }
                        ]
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response is not None
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert isinstance(response_body["data"]["create"]["id"], int)
    assert response_body.get("errors") is None


@mark.graphql
@mark.mutation
def test_create_invalid() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            mutation {
                create(
                    carrierInput: {
                        name: ""
                        nation: ""
                        carrierType: AIRCRAFT_CARRIER
                        commandcenter: {
                            codeName: ""
                            securityLevel: 999
                        }
                        aircrafts: [
                            {
                                model: ""
                                manufacturer: ""
                            }
                        ]
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"] is None
    errors: Final = response_body["errors"]
    assert isinstance(errors, list)
    assert len(errors) == 1
