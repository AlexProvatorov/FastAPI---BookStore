from sqlalchemy import text
from src.database import sync_engine, async_engine
from src.db.models.users import metadata


def create_tables():
    metadata.create_all(async_engine)
