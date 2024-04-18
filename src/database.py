import asyncio

from sqlalchemy import create_engine, URL, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg2,
    echo=settings.DEBUG,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=settings.DEBUG,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
)

#
# with sync_engine.connect() as connection:
#     res = connection.execute(text("SELECT 1, 2, 3 UNION SELECT 4, 5, 6"))
#     print(f"{res.all()[0]=}")
#
#
# async def get_456():
#     async with async_engine.connect() as connection:
#         res = await connection.execute(text("SELECT 1, 2, 3 UNION SELECT 4, 5, 6"))
#         print(f"{res.all()[1]=}")
#
#
# asyncio.run(get_456())
