import pytest
from fastapi.testclient import TestClient

from app.main import app, notes


@pytest.fixture
def client():
    notes.clear()
    with TestClient(app) as test_client:
        yield test_client
    notes.clear()
