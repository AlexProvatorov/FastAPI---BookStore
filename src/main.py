import uvicorn

from fastapi import FastAPI

from apps.auth.auth import auth_backend
from auth_utils import fastapi_users
from apps.auth.schemas import UserRead, UserCreate

from api.books import router as books_list
from api.tags import router as tags_list
from api.authors import router as authors_list
from exceptions import ExceptionBookstore
from handlers import handle_exception_bookstore


app = FastAPI(
    title="BookStore API",
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

app.add_exception_handler(ExceptionBookstore, handle_exception_bookstore)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
