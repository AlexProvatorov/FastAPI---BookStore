from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from db.models.goods import Tag

from apps.goods.schemas import TagCreate

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/")
async def get_tags(session: AsyncSession = Depends(get_async_session)):
    query = select(Tag)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{tag_id}")
async def get_tag(tag_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Tag).where(tag_id == Tag.id)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/")
async def add_tag(new_tag: TagCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Tag).values(**new_tag.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.patch("/{tag_id}")
async def edit_tag(tag_id: int, new_tag: TagCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Tag).values(**new_tag.dict()).where(tag_id == Tag.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete(
    path="/{tag_id}",
    name="Delete tag",
    description="Remove tag from tags list",
    status_code=204,
)
async def delete_tag(tag_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Tag).where(tag_id == Tag.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

