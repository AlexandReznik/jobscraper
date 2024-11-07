from unittest.mock import patch

import pytest

from app.common.jwt import create_token, decode_token


SECRET_KEY = "test-secret"
ALGORITHM = "HS256"


@pytest.fixture
def mock_encode():
    with patch("app.common.jwt.jwt.encode") as mock:
        yield mock


@pytest.fixture
def mock_decode():
    with patch("app.common.jwt.jwt.decode") as mock:
        yield mock


def test_create_token(mock_encode):
    mock_encode.return_value = "mocked-token"
    data = {"sub": "test@example.com"}
    token = create_token(data)
    assert isinstance(token, str)
    assert token == "mocked-token"
    mock_encode.assert_called_once()


def test_decode_token(mock_decode):
    data = {"sub": "test@example.com"}
    token = "mocked-token"
    mock_decode.return_value = data
    decoded_data = decode_token(token)
    assert decoded_data["sub"] == data["sub"]
    mock_decode.assert_called_once()


@pytest.mark.parametrize("exception_type", [ValueError, KeyError])
def test_decode_invalid_token(mock_decode, exception_type):
    mock_decode.side_effect = exception_type("Invalid token")
    with pytest.raises(exception_type):
        decode_token("invalid-token")
    mock_decode.assert_called_once()