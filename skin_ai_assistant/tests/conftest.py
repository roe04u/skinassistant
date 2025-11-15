import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture(scope="session")
def client():
    """
    Shared FastAPI TestClient for all tests.
    Uses the real app with SQLite DB.
    """
    return TestClient(app)
