from test.utils import *
from routers.auth import (
    ALGORITHM,
    SECRET_KEY,
    get_db,
    get_current_user,
    authenticate_user,
    create_access_token,
)
from jose import jwt
from fastapi import status, HTTPException
from datetime import timedelta
import pytest

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticate(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_authenticated_user = authenticate_user("WrongUserName", "wrongpassword", db)
    assert non_authenticated_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False

    def test_create_access_token(test_user):
        username = ("suri",)
        user_id = (1,)
        role = ("user",)
        expires_delta = timedelta(days=1)

        token = create_access_token(username, user_id, role, expires_delta)
        decoded_token = jwt.decode(
            token, SECRET_KEY, algorithms=ALGORITHM, options=("verify_signature", False)
        )
        assert decoded_token.get("sub") == username
        assert decoded_token.get("id") == user_id
        assert decoded_token.get("role") == role


@pytest.mark.anyio
async def test_get_current_user_valid_token():
    encode = {"sub": "test_user", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {"username": "test_user", "id": 1, "user_role": "admin"}


@pytest.mark.anyio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate user"
