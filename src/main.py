import os
import sys

import uvicorn

from apps.auth.database import User

from fastapi_users import fastapi_users, FastAPIUsers


from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi_users import fastapi_users
from fastapi import FastAPI
from pydantic import BaseModel, Field

from apps.auth.auth import auth_backend
from apps.auth.manager import get_user_manager
from apps.auth.schemas import UserRead, UserCreate

from api.books import router as books_list
from api.tags import router as tags_list
from api.authors import router as authors_list

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
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)


app.include_router(books_list)
app.include_router(tags_list)
app.include_router(authors_list)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
