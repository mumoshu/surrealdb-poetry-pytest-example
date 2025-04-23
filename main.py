"""Main application script."""
import asyncio
from surrealdb import AsyncSurreal

async def main():
    """Connects to SurrealDB and performs example operations."""
    async with AsyncSurreal("ws://surrealdb:8000") as db:
        await db.signin({"username": "root", "password": "root"})
        await db.use("test", "test") # Use namespace 'test', database 'test'
        print("Connected to SurrealDB!")
        # ... your database operations here ...

if __name__ == "__main__":
    asyncio.run(main())
