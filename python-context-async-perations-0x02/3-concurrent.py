
import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        result = await cursor.fetchall()
        return result

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        result = await cursor.fetchall()
        return result

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:", results[0])
    print("Users older than 40:", results[1])

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
