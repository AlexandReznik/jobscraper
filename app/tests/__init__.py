from unittest.mock import MagicMock
from app.common.database import get_db
from app.main import app


def override_get_db():
    db = MagicMock()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db