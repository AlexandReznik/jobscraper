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
def test_create_user(mock_create_user: MagicMock, mock_get_user_by_email: MagicMock, 
                     client: TestClient, db_session: Session, mock_user):
    mock_get_user_by_email.return_value = None
    user_data = {
        "email": "user@example.com",
        "preferences": "Django,Python"
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


@patch("app.users.crud.get_users")
def test_read_events_endpoint(mock_get_users: MagicMock, 
                              client: TestClient, mock_users):
    mock_get_users.return_value = mock_users
    response = client.get("/users/all/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == "user@example.com"
    assert response.json()[1]["email"] == "user1@example.com"


@patch("app.jobs.crud.get_jobs")
def test_read_jobs_endpoint(mock_get_jobs: MagicMock, client: TestClient, db_session: Session):
    mock_get_jobs.return_value.status_code = 200
    response = client.get("/jobs/all/")
    assert response.status_code == 200