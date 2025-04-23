"""Tests for SurrealDB index operations."""
import pytest
from surrealdb import AsyncSurreal

@pytest.mark.asyncio
async def test_index_operations(db: AsyncSurreal):
    """Tests checking, creating, and removing indices."""
    table_name = "test_index_table"
    index_name = "user_email_index"
    field_name = "email"

    try:
        # Setup: Define table
        await db.query(f"DEFINE TABLE {table_name} SCHEMAFULL;")
        await db.query(f"DEFINE FIELD {field_name} ON {table_name} TYPE string;")
        print(f"Defined table {table_name} with field {field_name}")
        
        # 1. Check Index Existence (Initially should not exist)
        table_info_before = await db.query(f"INFO FOR TABLE {table_name};")
        # Crude check, refine based on actual output format
        assert f"index {index_name}" not in str(table_info_before).lower(), "Index found before creation"
        print(f"Verified index {index_name} does not exist initially")

        # 2. Create Index
        await db.query(f"DEFINE INDEX {index_name} ON TABLE {table_name} COLUMNS {field_name} UNIQUE;")
        print(f"Defined UNIQUE index {index_name} on {table_name}({field_name})")
        
        # 3. Check Index Existence (Should exist now)
        # Allow some time for index creation if necessary, though usually fast
        # await asyncio.sleep(0.1) 
        table_info_after = await db.query(f"INFO FOR TABLE {table_name};")
        assert f"index {index_name}" in str(table_info_after).lower(), "Index not found after creation"
        # A more robust check might parse the `indexes` part of the info response
        print(f"Verified index {index_name} exists after creation")

        # 4. Remove Index
        await db.query(f"REMOVE INDEX {index_name} ON TABLE {table_name};")
        print(f"Removed index {index_name} on {table_name}")

        # 5. Check Index Existence (Should not exist anymore)
        table_info_final = await db.query(f"INFO FOR TABLE {table_name};")
        assert f"index {index_name}" not in str(table_info_final).lower(), "Index still found after removal"
        print(f"Verified index {index_name} does not exist after removal")

    finally:
        # Cleanup
        await db.query(f"REMOVE TABLE {table_name};")
        print(f"Cleaned up table {table_name}") 