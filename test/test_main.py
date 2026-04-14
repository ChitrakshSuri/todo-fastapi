from fastapi.testclient import TestClient
import main
from fastapi import status
from routers.auth import create_access_token
from datetime import timedelta

client = TestClient(main.app)


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_root_redirects_logged_out_users_to_login():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.headers["location"] == "/auth/login-page"


def test_root_redirects_logged_in_users_to_todos():
    token = create_access_token("suri", 1, "admin", timedelta(minutes=20))
    response = client.get(
        "/",
        cookies={"access_token": token},
        follow_redirects=False,
    )
    assert response.status_code == status.HTTP_302_FOUND
    assert response.headers["location"] == "/todos/todo-page"
