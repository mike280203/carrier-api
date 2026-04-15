# ruff: noqa: S101, D103

"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login
from httpx import post
from pytest import mark


@mark.graphql
@mark.query
def test_query_id() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                carrier(carrierId: "1000") {
                    id
                    version
                    name
                    nation
                    carrierType
                    commandcenter {
                        codeName
                        securityLevel
                    }
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
    data: Final = response_body["data"]
    assert data is not None
    carrier: Final = data["carrier"]
    assert isinstance(carrier, dict)
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_id_notfound() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                carrier(carrierId: "999999") {
                    name
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
    assert response_body["data"]["carrier"] is None
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_name() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                carriers(suchparameter: {name: "USS Gerald R. Ford"}) {
                    id
                    version
                    name
                    nation
                    carrierType
                    commandcenter {
                        codeName
                        securityLevel
                    }
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
    carriers: Final = response_body["data"]["carriers"]
    assert isinstance(carriers, list)
    assert len(carriers) > 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_name_notfound() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                carriers(suchparameter: {name: "NichtVorhanden"}) {
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
    carriers: Final = response_body["data"]["carriers"]
    assert isinstance(carriers, list)
    assert len(carriers) == 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_nation() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                carriers(suchparameter: {nation: "USA"}) {
                    id
                    version
                    name
                    nation
                    carrierType
                    commandcenter {
                        codeName
                        securityLevel
                    }
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
    carriers: Final = response_body["data"]["carriers"]
    assert isinstance(carriers, list)
    assert len(carriers) > 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_nation_notfound() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                carriers(suchparameter: {nation: "Atlantis"}) {
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
    carriers: Final = response_body["data"]["carriers"]
    assert isinstance(carriers, list)
    assert len(carriers) == 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_carrier_type() -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                carriers(suchparameter: {carrierType: AIRCRAFT_CARRIER}) {
                    id
                    name
                    nation
                    carrierType
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
    carriers: Final = response_body["data"]["carriers"]
    assert isinstance(carriers, list)
    assert len(carriers) > 0
    assert response_body.get("errors") is None
