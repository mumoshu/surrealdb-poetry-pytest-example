"""Tests for SurrealDB field operations."""
import pytest
from surrealdb import AsyncSurreal

@pytest.mark.asyncio
async def test_field_operations(db: AsyncSurreal):
    """Tests fetching, adding, and removing fields from a schemaful table."""
    table_name = "test_field_ops_table"
    
    try:
        # Setup: Define table
        await db.query(f"DEFINE TABLE {table_name} SCHEMAFULL;")
        await db.query(f"DEFINE FIELD initial_field ON {table_name} TYPE string;")
        print(f"Defined table {table_name} with field 'initial_field'")

        # 1. Fetch Fields (using INFORMATION query)
        schema_info = await db.query(f"INFO FOR TABLE {table_name};")
        assert "initial_field" in str(schema_info), "Initial field not found after definition"
        print("Verified initial_field exists")

        # 2. Add Field
        await db.query(f"DEFINE FIELD added_field ON {table_name} TYPE bool;")
        schema_info_after_add = await db.query(f"INFO FOR TABLE {table_name};")
        assert "added_field" in str(schema_info_after_add), "Added field not found"
        print("Added and verified added_field")

        # 3. Remove Field
        await db.query(f"REMOVE FIELD initial_field ON {table_name};")
        schema_info_after_remove = await db.query(f"INFO FOR TABLE {table_name};")
        assert "initial_field" not in str(schema_info_after_remove), "Initial field still found after removal"
        assert "added_field" in str(schema_info_after_remove), "Added field missing after removing initial_field"
        print("Removed initial_field and verified state")

    finally:
        # Cleanup
        await db.query(f"REMOVE TABLE {table_name};")
        print(f"Cleaned up table {table_name}") 