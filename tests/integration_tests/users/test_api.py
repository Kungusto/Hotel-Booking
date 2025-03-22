from src.schemas.users import UserRequestAdd
from pydantic import BaseModel
import pytest

async def test_auth(ac) : 
    # /auth/register
    data = UserRequestAdd(
        email="user@example.com", 
        name="John", 
        nickname="Johny312", 
        password="12345")
    register_response = await ac.post(
        url="/auth/register",
        json=data.model_dump()
    )
    user = register_response.json()["data"]
    # вычисляем какой код должен быть на выходе
    assert register_response.status_code == 200
    assert user

    # /auth/login
    auth_ac = await ac.post(
        url="/auth/login",
        json={
            "email":data.email,
            "password":data.password,
        }
    )
    assert auth_ac.status_code == 200
    assert ac.cookies
    assert "access_token" in ac.cookies


    # /auth/me
    all_bookings = await ac.get(
        url="/auth/me",
    )
    assert all_bookings.status_code == 200
    assert isinstance(all_bookings.json(), dict)

    # /auth/logout
    assert ac.cookies
    result_logout = await ac.post(
        url="/auth/logout",
    )
    assert result_logout.status_code == 200
    assert not ac.cookies