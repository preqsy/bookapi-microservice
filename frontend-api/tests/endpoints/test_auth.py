import pytest
from fastapi import status
from httpx import AsyncClient

from tests.sample_datas.auth_user_samples import (
    sample_auth_user_create,
    sample_auth_user_wrong_email,
    sample_header,
    sample_login_user,
    sample_login_user_wrong_email,
)


async def register_user(
    client: AsyncClient,
    sample_register_details: dict = sample_auth_user_create(),
):
    response = await client.post(
        "/auth/register",
        json=sample_register_details,
        headers=sample_header(),
    )

    return response


async def login_user(client, sample_login_details: dict = sample_login_user()):
    await register_user(client)

    rsp = await client.post(
        url="/auth/login",
        data=sample_login_details,
    )

    return rsp


@pytest.mark.asyncio
@pytest.mark.freeze_time("2024-07-23 08:45:00.650334")
async def test_register_success(
    client: AsyncClient,
):

    response = await register_user(client)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_register_wrong_email_format(client: AsyncClient):
    response = await register_user(
        client,
        sample_register_details=sample_auth_user_wrong_email(),
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await register_user(client)

    rsp = await login_user(client)

    assert rsp.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_login_incorrect_credentials(client: AsyncClient):
    await register_user(client)

    rsp = await login_user(client, sample_login_details=sample_login_user_wrong_email())

    assert rsp.status_code == status.HTTP_403_FORBIDDEN
