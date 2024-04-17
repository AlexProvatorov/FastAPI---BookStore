import os
import sys

from src.apps.auth.database import User

from fastapi_users import fastapi_users, FastAPIUsers

from db.core import create_tables

from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.apps.auth.auth import auth_backend
from src.apps.auth.manager import get_user_manager
from src.apps.auth.schemas import UserRead, UserCreate

# sys.path.insert(1, os.path.join(sys.path[0], '..'))


create_tables()


app = FastAPI(
    title="BookStore API",
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

fake_users = [
    {"id": 1, "name": "Alex", "role": "admin", "degree": [
        {"id": 1, "created_at": "2024-04-15T18:48:07.812Z", "type_degree": "master"}
    ]},
    {"id": 2, "name": "Bob", "role": "admin", "degree": None},
]


fake_books = [
    {"id": 1, "title": "Book1", "author": "ALex", "price": 100},
    {"id": 2, "title": "Book2", "author": "Bob", "price": 200},
    {"id": 3, "title": "Book3", "author": "Alice", "price": 300},
]


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


class DegreeType(Enum):
    novice = "novice"
    medium = "medium"
    master = "master"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]]


class Book(BaseModel):
    id: int
    title: str = Field(max_length=255)
    author: str = Field(max_length=255)
    price: float = Field(ge=0)


@app.get("/users/{user_id}", response_model=List[User])
async def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


@app.get("/users")
async def get_users(limit: int = 1, offset: int = 0):
    return fake_users[offset:][:limit]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def say_hello(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_id": item_id}


@app.post("/books")
async def add_books(books: list[Book]):
    fake_books.extend(books)
    return {"status": 200, "data": fake_books}
