from src.schemas.users import UserRequestAdd
from pydantic import BaseModel
import pytest

@pytest.mark.parametrize("email, name, nickname, password, status_code", [
    ("user@example.com", "John", "Johny312", "12345", 200),
    ("user@example.com", "John", "Johny312", "12345", 400),
    ("бу!", "John", "Johny312", "12345", 422),
])
async def test_auth(
        ac,
        email: int, name: str, nickname: str, password: str, status_code: int
    ) : 
    # /auth/register
    register_response = await ac.post(
        url="/auth/register",
        json={
            "email":email,
            "name":name,
            "nickname":nickname,
            "password":password
        }
    )
    # вычисляем какой код должен быть на выходе
    assert register_response.status_code == status_code
    if status_code != 200 : 
        return
    user = register_response.json()["data"]
    assert user

    # /auth/login
    auth_ac = await ac.post(
        url="/auth/login",
        json={
            "email":email,
            "password":password,
        }
    )
    assert auth_ac.status_code == 200
    assert ac.cookies
    assert "access_token" in ac.cookies


    # /auth/me
    all_bookings = await ac.get(
        url="/auth/me",
    )
    current_user_data = all_bookings.json()
    assert all_bookings.status_code == 200
    assert isinstance(current_user_data, dict)
    assert "password" not in current_user_data
    assert "hashed_password" not in current_user_data

    # /auth/logout
    assert ac.cookies
    result_logout = await ac.post(
        url="/auth/logout",
    )
    assert result_logout.status_code == 200
    assert not ac.cookies