from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from app.users import crud


@pytest.fixture
def db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_user():
    return MagicMock(id=1, email="user@example.com", preferences="Django, Python")


@pytest.fixture
def user_create():
    return MagicMock(email="user@example.com", preferences="Django, Python", password="password")


@patch("app.common.database.create_engine")
def test_get_user_by_email(db_session, mock_user):
    db_session.query().filter().first.return_value = mock_user
    result = crud.get_user_by_email(db_session, email="user@example.com")
    db_session.query().filter().first.assert_called_once()
    assert result == mock_user


@patch("app.common.database.create_engine")
def test_create_user(db_session, user_create):
    with patch("app.users.crud.get_password_hash", return_value="hashedpassword"):
        result = crud.create_user(db_session, user_create)
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()
    assert result.email == user_create.email
    assert result.password == "hashedpassword"


@patch("app.common.database.create_engine")
def test_get_user(db_session, mock_user):
    db_session.query().filter().first.return_value = mock_user
    result = crud.get_user(db_session, user_id=mock_user.id)
    db_session.query().filter().first.assert_called_once()
    assert result == mock_user


@patch("app.common.database.create_engine")
def test_get_users(db_session, mock_user):
    db_users = [mock_user, MagicMock(id=2, email="anotheruser@example.com", 
                                     preferences="Flask, JavaScript")]
    db_session.query().all.return_value = db_users
    result = crud.get_users(db_session)
    db_session.query().all.assert_called_once()
    assert result == db_users