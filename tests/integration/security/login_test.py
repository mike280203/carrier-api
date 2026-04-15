# ruff: noqa: S101, D103

"""Tests für Login."""

from http import HTTPStatus
from typing import Final

from common_test import (
    base_url,
    ctx,
    login,
    password_user,
    timeout,
    token_path,
    username_admin,
    username_user,
)
from httpx import post
from pytest import mark


@mark.login
def test_login_admin() -> None:
    token: Final = login()

    assert isinstance(token, str)
    assert token


@mark.login
def test_login_user() -> None:
    token: Final = login(username=username_user, password=password_user)

    assert isinstance(token, str)
    assert token


@mark.login
def test_login_falsches_passwort() -> None:
    login_data: Final = {
        "username": username_admin,
        "password": "FALSCHES_PASSWORT",
    }

    response: Final = post(
        f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.login
def test_login_ohne_daten() -> None:
    login_data: dict[str, str] = {}

    response: Final = post(
        f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
