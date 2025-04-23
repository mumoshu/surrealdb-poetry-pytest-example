"""Tests for SurrealDB connection."""
import pytest
from surrealdb import AsyncSurreal

# Configuration constants are now in conftest.py
# The db_conn fixture (providing isolated DB) is also in conftest.py


@pytest.mark.asyncio
async def test_surrealdb_connection(db: AsyncSurreal):
    """
    Tests the connection to the SurrealDB instance using the shared db_conn fixture.
    Verifies that basic info can be retrieved within the test-specific DB.
    """
    try:
        # The fixture already connected, signed in, and selected a unique DB
        info = await db.info() # Use the connected db_conn instance
        assert info is None # Basic check that info was returned
        # Try to create a new table and check non-empty info
        await db.query("DEFINE TABLE test_table;")
        info = await db.query("INFO FOR TABLE test_table;")
        assert info is not None # Check that info is now non-empty
        print(f"\nSuccessfully connected and got info via fixture. DB Info: {info}")

    except Exception as e:
        pytest.fail(f"Failed to get info via shared fixture: {e}")

# No other tests in this file
