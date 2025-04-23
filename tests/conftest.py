"""Shared fixtures for pytest."""
import pytest
import pytest_asyncio
from surrealdb import AsyncSurreal
import re

# Configuration for the SurrealDB connection (shared across tests)
DB_URL = "ws://surrealdb:8000"
DB_USER = "root"
DB_PASS = "root"
DB_NAMESPACE = "test"
# Default DB_DATABASE removed as each test gets its own

@pytest_asyncio.fixture(scope="function")
async def db(request):
    """Provides an initialized SurrealDB client fixture connected to a unique DB per test."""
    base_name = request.function.__name__.lower()
    db_name = re.sub(r'\W|^(?=\d)', '_', base_name)
    db_name = f"test_db_{db_name[:30]}"

    client = AsyncSurreal(url=DB_URL)
    try:
        await client.signin({"username": DB_USER, "password": DB_PASS})
        await client.use(DB_NAMESPACE, db_name)
        print(f"\n--- Connected & Using DB: {db_name} for test {request.function.__name__} ---")
        yield client # Yield the connected client instance
    finally:
        # Teardown Part 1: Close the main client connection
        print(f"\n--- Closing main connection for test {request.function.__name__} ---")
        if client: # Check if client was successfully created
            await client.close()
            print("Main connection closed.")
        
        # Teardown Part 2: Clean up the specific database created for this test
        print(f"--- Tearing down DB: {db_name} for test {request.function.__name__} ---")
        try:
            # Use a separate temporary client for cleanup
            async with AsyncSurreal(url=DB_URL) as temp_client_for_cleanup:
                await temp_client_for_cleanup.signin({"username": DB_USER, "password": DB_PASS})
                await temp_client_for_cleanup.query(f"REMOVE DATABASE {db_name};")
                print(f"Removed database {db_name}.")
        except Exception as e: 
            print(f"Note: Error during database cleanup for {db_name}: {e}") 

# Removed the old module-scoped 'db' fixture 