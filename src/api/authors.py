from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from db.models.goods import Author

from apps.goods.schemas import AuthorCreate

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.get("/")
async def get_authors(session: AsyncSession = Depends(get_async_session)):
    query = select(Author)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{author_id}")
async def get_author(author_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Author).where(author_id == Author.id)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/")
async def add_author(new_author: AuthorCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Author).values(**new_author.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.patch("/{author_id}")
async def edit_author(author_id: int, new_author: AuthorCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Author).values(**new_author.dict()).where(author_id == Author.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/{author_id}")
async def delete_author(author_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Author).where(author_id == Author.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
