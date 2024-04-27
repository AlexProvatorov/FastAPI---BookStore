from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import current_superuser
from database import get_async_session
from db.models.goods import Author

from apps.goods.schemas import AuthorCreate
from exceptions import ExceptionNotFound

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.get(
    path="/",
    name="Get all authors",
    description="Get all authors from authors model",
    status_code=200,
)
async def get_authors(session: AsyncSession = Depends(get_async_session)):
    query = select(Author)
    result = await session.execute(query)
    authors = result.scalars().all()

    if not authors:
        raise ExceptionNotFound(message="Authors not found")

    return authors


@router.get(
    path="/{author_id}",
    name="Get one author",
    description="Get one author through id from authors model",
    status_code=200,
)
async def get_author(
    author_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(Author).where(author_id == Author.id)
    result = await session.execute(query)
    author = result.scalars().all()

    if not author:
        raise ExceptionNotFound(message="Author not found")

    return author


@router.post(
    path="/",
    name="Create new author",
    description="Create new author for authors model",
    response_model=AuthorCreate,
    status_code=201,
    dependencies=[Depends(current_superuser)]
)
async def add_author(
    new_author: AuthorCreate, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Author).values(**new_author.dict())
    await session.execute(stmt)
    await session.commit()
    return new_author


@router.patch(
    path="/{author_id}",
    name="Change author",
    description="Change author for authors model",
    response_model=AuthorCreate,
    status_code=201,
    dependencies=[Depends(current_superuser)]
)
async def edit_author(
    author_id: int,
    changed_author: AuthorCreate,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Author).where(author_id == Author.id)
    result = await session.execute(query)
    author = result.scalars().first()

    if not author:
        raise ExceptionNotFound(message="Author not found")

    stmt = update(Author).values(**changed_author.dict()).where(author_id == Author.id)
    await session.execute(stmt)
    await session.commit()
    return changed_author


@router.delete(
    path="/{author_id}",
    name="Delete one book",
    description="Remove one book through id from books model",
    response_model=None,
    status_code=204,
    dependencies=[Depends(current_superuser)]
)
async def delete_author(
    author_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(Author).where(author_id == Author.id)
    result = await session.execute(query)
    author = result.scalars().first()

    if not author:
        raise ExceptionNotFound(message="Author not found")

    stmt = delete(Author).where(author_id == Author.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
