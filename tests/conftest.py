
import os
import pytest
from fastapi.testclient import TestClient
import sqlite_utils

# Set a dummy API key for testing before importing the apps
# This ensures the services can be imported without raising an error
os.environ["SANCTUM_API_KEY"] = "test-key"

from src.pivot_service import app as pivot_app
from src.cme_service import app as cme_app, DB_PATH

@pytest.fixture(scope="module")
def pivot_client():
    """Fixture for the Pivot Service test client."""
    with TestClient(pivot_app) as c:
        yield c

@pytest.fixture(scope="module")
def cme_client():
    """
    Fixture for the CME Service test client.
    Handles module-level setup and teardown of the test database.
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH) # Ensure clean slate before module tests
    
    # The TestClient context manager handles app startup/shutdown
    with TestClient(cme_app) as c:
        yield c
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH) # Clean up after all tests in the module are done

@pytest.fixture(autouse=True)
def clear_db_before_each_test():
    """
    Fixture to clear the verses table before each test function.
    This runs automatically for all tests due to `autouse=True`.
    """
    # Check if DB_PATH was created by cme_client startup
    if os.path.exists(DB_PATH):
        db = sqlite_utils.Database(DB_PATH)
        if "verses" in db.table_names():
            db["verses"].delete_where()
