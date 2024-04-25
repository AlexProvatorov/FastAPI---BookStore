from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DECIMAL, DateTime, func, Table, Date
from sqlalchemy.orm import relationship

from database import Base


class TagOfBooks(Base):
    __tablename__ = 'tags_of_books'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('books.id'))
    id_tag = Column(Integer, ForeignKey('tags.id'))


class AuthorOfBooks(Base):
    __tablename__ = 'authors_of_books'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('books.id'))
    id_author = Column(Integer, ForeignKey('tags.id'))


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    cost = Column(DECIMAL, nullable=False)
    count_in_stock = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    photo = Column(String, default=None, nullable=False)
    date_released = Column(Date)

    tags = relationship(
        'Tag',
        primaryjoin="Book.id == TagOfBooks.id_book",
        secondaryjoin="TagOfBooks.id_tag == Tag.id",
        secondary='tags_of_books',
        backref='books',
        lazy='selectin',
    )
    authors = relationship(
        'Author',
        primaryjoin="Book.id == AuthorOfBooks.id_book",
        secondaryjoin="AuthorOfBooks.id_author == Author.id",
        secondary='authors_of_books',
        backref='books',
        lazy='selectin',
    )


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
