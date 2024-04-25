from datetime import datetime
from typing import List

from pydantic import BaseModel
from decimal import Decimal


class Book(BaseModel):
    name: str
    description: str
    slug: str
    cost: Decimal
    count_in_stock: int
    is_active: bool
    photo: str
    date_released: datetime

    class Config:
        orm_mode = True


class BookCreate(Book):
    tags: List[int]
    authors: List[int]


class TagCreate(BaseModel):
    name: str
    description: str
    slug: str

    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class BookOut(BookCreate):
    tags: List[TagCreate]


class TagOut(TagCreate):
    books: List[BookCreate]


class BookOut2(BookCreate):
    authors: List[AuthorCreate]


class AuthorOut(AuthorCreate):
    books: List[BookCreate]


class AuthorOfBook(BaseModel):
    id_author: int
    id_book: int

    class Config:
        orm_mode = True


class TagOfBook(BaseModel):
    id_tag: int
    id_book: int

    class Config:
        orm_mode = True
