import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from sqlalchemy.orm import Session
from app.users import models


@pytest.fixture
def db_session():
    return MagicMock(spec=Session)


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    user.email = "user@example.com"
    user.preferences = "Django,Python"
    return user


@pytest.fixture
def mock_users():
    return [
        models.User(
            id=1,
            email="user@example.com",
            preferences="Django"
        ),
        models.User(
            id=2,
            email="user1@example.com",
            preferences="Flask"
        )
    ]


@patch("app.users.crud.get_user_by_email")
@patch("app.users.crud.create_user")
@patch("app.common.security.get_password_hash")
def test_create_user(mock_get_password_hash: MagicMock, mock_create_user: MagicMock, 
                     mock_get_user_by_email: MagicMock, 
                     client: TestClient, db_session: Session, mock_user):
    mock_get_user_by_email.return_value = None
    mock_get_password_hash.return_value = "hashed_secret"
    user_data = {
        "email": "user@example.com",
        "preferences": "Django,Python",
        "password": "secret"
    }   
    mock_create_user.return_value = mock_user
    response = client.post("/users/create/", json=user_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "user@example.com",
        "preferences": "Django,Python"
    }
    mock_create_user.assert_called_once()


@patch("app.users.crud.decode_token")
@patch("app.users.crud.get_user_by_email")
def test_get_current_user_me_valid_token(mock_get_user_by_email: MagicMock, 
                                         mock_decode_token: MagicMock, 
                                         mock_user, client: TestClient):
    mock_decode_token.return_value = {"sub": "johndoe@example.com"}
    mock_get_user_by_email.return_value = mock_user
    response = client.post("/users/me/", headers={"Authorization": "Bearer valid-token"})
    assert response.status_code == 200
    assert response.json() == {
        "email": "user@example.com",
        "preferences": "Django,Python"
    }
    mock_decode_token.assert_called_once_with("valid-token")


@patch("app.users.crud.decode_token")
@patch("app.jobs.crud.get_jobs")
def test_read_jobs_endpoint(mock_get_jobs: MagicMock, mock_decode_token: MagicMock, client: TestClient, db_session: Session):
    mock_get_jobs.return_value.status_code = 200
    mock_decode_token.return_value = {"sub": "johndoe@example.com"}
    response = client.get("/jobs/all/", headers={"Authorization": "Bearer valid-token"})
    assert response.status_code == 200