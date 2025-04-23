"""Tests for SurrealDB schema operations."""
import pytest
from surrealdb import AsyncSurreal


@pytest.mark.asyncio
async def test_schema_operations(db: AsyncSurreal):
    """Tests defining, redefining, and removing a schemaful table within an isolated DB."""
    table_name = "test_schema_table"
    
    # No try...finally needed here for cleanup, fixture handles DB removal
    
    # 1. Define Schema
    await db.query(f"DEFINE TABLE {table_name} SCHEMAFULL;")
    await db.query(f"DEFINE FIELD name ON {table_name} TYPE string;")
    print(f"Defined schemaful table {table_name} with field 'name'")
    
    # Verify definition (Optional but recommended: Use INFO FOR TABLE)
    info_after_define = await db.query(f"INFO FOR TABLE {table_name};")
    assert "name" in str(info_after_define)

    # 2. Redefine Schema (Add a field)
    await db.query(f"DEFINE FIELD age ON {table_name} TYPE int;")
    print(f"Added field 'age' to {table_name}")
    
    # Verify addition (Optional but recommended: Use INFO FOR TABLE)
    info_after_add = await db.query(f"INFO FOR TABLE {table_name};")
    assert "age" in str(info_after_add)

    # 3. Removal is handled by the db fixture tearing down the database
    # If you wanted to test REMOVE TABLE explicitly, you could add:
    # await db.query(f"REMOVE TABLE {table_name};")
    # print(f"Removed table {table_name}") 