"""Tests for SurrealDB record operations (CRUD)."""
import pytest
from surrealdb import AsyncSurreal, RecordID

@pytest.mark.asyncio
async def test_record_operations(db: AsyncSurreal):
    """Tests creating, updating, selecting, and deleting records."""
    table_name = "test_record_table" # Using a schemaless table for simplicity
    record_id = f"{table_name}:test1"
    record_data_initial = {"name": "Test User", "status": "active"}
    record_data_update = {"status": "inactive", "level": 5}

    try:
        # 1. Create Record
        created_list = await db.create(table_name, record_data_initial)
        # create can return a list if data is a list, we assume single dict here
        # Adjust if creating multiple records at once
        created = created_list[0] if isinstance(created_list, list) else created_list 
        record_id = created['id'] # Get the actual ID assigned by SurrealDB
        print(f"Created record {record_id} with data: {record_data_initial}")
        assert created is not None
        assert created["name"] == record_data_initial["name"]
        assert created["status"] == record_data_initial["status"]

        # 2. Select Record (Verify Create)
        selected = await db.select(record_id)
        print(f"Selected record {record_id}: {selected}")
        assert selected is not None
        assert selected["name"] == record_data_initial["name"]

        # 3. Update Record
        # Note: update() replaces the record content by default.
        # Use merge() if you want to merge fields.
        updated_list = await db.update(record_id, record_data_update) 
        updated = updated_list[0] if isinstance(updated_list, list) else updated_list
        print(f"Updated record {record_id} with data: {record_data_update}")
        assert updated is not None
        assert updated["status"] == record_data_update["status"]
        assert updated["level"] == record_data_update["level"]
        # Verify original fields not present unless merged
        assert "name" not in updated 

        # 4. Select Record (Verify Update)
        selected_after_update = await db.select(record_id)
        print(f"Selected record {record_id} after update: {selected_after_update}")
        assert selected_after_update["status"] == record_data_update["status"]
        assert "name" not in selected_after_update

        # 5. Delete Record
        # delete() returns the deleted record(s)
        deleted_list = await db.delete(record_id)
        deleted = deleted_list[0] if isinstance(deleted_list, list) else deleted_list
        print(f"Deleted record {record_id}: {deleted}")
        assert deleted is not None 
        assert deleted["id"] == record_id

        # 6. Select Record (Verify Delete)
        selected_after_delete = await db.select(record_id)
        print(f"Selected record {record_id} after delete: {selected_after_delete}")
        assert selected_after_delete is None

    finally:
        # Cleanup is implicitly handled by the fixture for this table 
        # (if test_record_table is added to fixture cleanup)
        # If not using fixture cleanup, add: await db.query(f"REMOVE TABLE {table_name};")
        pass

@pytest.mark.asyncio
async def test_record_upsert(db: AsyncSurreal):
    """Tests upserting records (create or update)."""
    table_name = "test_upsert_table" 
    record_id = f"{table_name}:upsert1"
    initial_data = {"value": 100}
    update_data = {"value": 200, "new_field": True}

    try:
        # 1. Upsert (Create)
        upserted1_list = await db.upsert(record_id, initial_data)
        upserted1 = upserted1_list[0] if isinstance(upserted1_list, list) else upserted1_list
        print(f"Upserted (create) {record_id}: {upserted1}")
        assert upserted1["value"] == initial_data["value"]
        assert upserted1["id"] == RecordID(table_name, "upsert1")

        # 2. Upsert (Update/Merge)
        upserted2_list = await db.upsert(record_id, update_data)
        upserted2 = upserted2_list[0] if isinstance(upserted2_list, list) else upserted2_list
        print(f"Upserted (update) {record_id}: {upserted2}")
        assert upserted2["value"] == update_data["value"]
        assert upserted2["new_field"] == update_data["new_field"]
        assert upserted2["id"] == RecordID(table_name, "upsert1")

        # 3. Verify final state
        # Note that db.select(f"{table_name}:upsert1") will end up returning empty list.
        # Perhaps it's inconsistency in the SurrealDB Python client that it does understand table:id thing in some methods
        # but not in others.
        final_select = await db.select(RecordID(table_name, "upsert1"))
        assert final_select["value"] == update_data["value"]
        assert final_select["new_field"] == update_data["new_field"]
    
    finally:
        # Cleanup
        await db.query(f"REMOVE TABLE {table_name};") # Remove the specific table for this test
        print(f"Cleaned up table {table_name}") 