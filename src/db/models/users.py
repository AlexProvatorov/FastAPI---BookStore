from sqlalchemy import MetaData, Table, Column, String, TIMESTAMP, Integer, Boolean


metadata = MetaData()


user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String(length=320), unique=True, nullable=False, index=True),
    Column('username', String(length=255), unique=True, nullable=False),
    Column('hashed_password', String(length=1024), nullable=False),
    Column('photo', String(length=255), nullable=True),
    Column('first_name', String(length=255), nullable=True),
    Column('last_name', String(length=255), nullable=True),
    Column('date_of_birth', TIMESTAMP, nullable=True, unique=False),
    Column('slug', String(length=255), nullable=False, unique=True),
    Column('is_active', Boolean, nullable=False, default=True),
    Column('is_superuser', Boolean, nullable=False, default=False),
    Column('is_verified', Boolean, nullable=False, default=False),

)
