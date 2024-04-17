# from datetime import datetime
#
# from sqlalchemy import MetaData, Table, Column, String, TIMESTAMP, ForeignKey, Integer, Boolean
#
# metadata = MetaData()
#
#
# items = Table(
#     'items',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('name', String, nullable=False),
#     Column('description', String, nullable=False),
#     Column('slug', String, unique=True, nullable=False),
#     Column('cost', Integer, nullable=False),
#     Column('count_in_stock', Integer, nullable=False),
#     Column('is_active', Boolean, nullable=False, default=True),
#     Column('time_created', TIMESTAMP, default=datetime.utcnow),
#     Column('time_updated', TIMESTAMP, nullable=True, default=datetime.utcnow),
#     Column('photo', ),
#     Column('tags'),
# )
#
#
# tags = Table(
#     'tags',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('name', String, nullable=False),
#     Column('slug', String, unique=True, nullable=False),
#     Column('description', String, nullable=False),
# )
#
#
# authors = Table(
#     'authors',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('first_name', String, nullable=False),
#     Column('last_name', String, nullable=False),
# )
#
#
# books = Table(
#     'books',
#     metadata,
#     Column('authors', Integer, ForeignKey('authors.id'), nullable=False),
#     Column('date_released', TIMESTAMP, default=datetime.date),
# )
