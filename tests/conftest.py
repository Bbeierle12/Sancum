
import os
import pytest
from fastapi.testclient import TestClient
import sqlite_utils
import tempfile

# Set a dummy API key for testing before importing the apps
# This ensures the services can be imported without raising an error
os.environ["SANCTUM_API_KEY"] = "test-key"

from src.pivot_service import app as pivot_app
from src.cme_service import app as cme_app
from src import cme_service, db as review_db


@pytest.fixture(scope="module")
def pivot_client():
    """Fixture for the Pivot Service test client."""
    with TestClient(pivot_app) as c:
        yield c

@pytest.fixture(scope="function")
def cme_client(monkeypatch):
    """
    Fixture for the CME Service test client.
    Creates a temporary, isolated database for each test function.
    """
    # Create a temporary file to act as the database
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name
    
    # Use monkeypatch to redirect DB_PATH constants in the relevant modules
    monkeypatch.setattr(cme_service, "DB_PATH", db_path)
    monkeypatch.setattr(review_db, "DB_PATH", db_path)

    # The TestClient context manager handles app startup/shutdown,
    # which will create the tables in our temporary database.
    with TestClient(cme_app) as c:
        yield c
    
    # Teardown: remove the temporary database file after the test is done
    if os.path.exists(db_path):
        os.remove(db_path)
