from sqlalchemy import text
from database import sync_engine, async_engine
from db.models.users import metadata


def create_tables():
    metadata.create_all(async_engine)
