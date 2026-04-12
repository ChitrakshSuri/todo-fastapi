from test.utils import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users/get_user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "suri"
    assert response.json()["email"] == "suri@suri.com"
    assert response.json()["first_name"] == "chit"
    assert response.json()["last_name"] == "suri"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "1234567890"