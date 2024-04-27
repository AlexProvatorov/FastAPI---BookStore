from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import current_superuser
from database import get_async_session
from db.models.goods import Tag

from apps.goods.schemas import TagCreate
from exceptions import ExceptionNotFound

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get(
    path="/",
    name="Get all tags",
    description="Get all tags from tags model",
    status_code=200,
)
async def get_tags(session: AsyncSession = Depends(get_async_session)):
    query = select(Tag)
    result = await session.execute(query)
    tags = result.scalars().all()

    if not tags:
        raise ExceptionNotFound(message="Tags not found")

    return tags


@router.get(
    path="/{tag_id}",
    name="Get one tag",
    description="Get one tag through id from tags model",
    status_code=200,
)
async def get_tag(tag_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Tag).where(tag_id == Tag.id)
    result = await session.execute(query)
    tag = result.scalars().all()

    if not tag:
        raise ExceptionNotFound(message="Tag not found")

    return tag


@router.post(
    path="/",
    name="Create new tag",
    description="Create new tag for tags model",
    response_model=TagCreate,
    status_code=201,
    dependencies=[Depends(current_superuser)]
)
async def add_tag(
    new_tag: TagCreate, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Tag).values(**new_tag.dict())
    await session.execute(stmt)
    await session.commit()
    return new_tag


@router.patch(
    path="/{tag_id}",
    name="Change tag",
    description="Change tag for tags model",
    response_model=TagCreate,
    status_code=201,
    dependencies=[Depends(current_superuser)]
)
async def edit_tag(
    tag_id: int,
    changed_tag: TagCreate,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Tag).where(tag_id == Tag.id)
    result = await session.execute(query)
    tag = result.scalars().first()

    if not tag:
        raise ExceptionNotFound(message="Tag not found")

    stmt = update(Tag).values(**changed_tag.dict()).where(tag_id == Tag.id)
    await session.execute(stmt)
    await session.commit()
    return changed_tag


@router.delete(
    path="/{tag_id}",
    name="Delete one tag",
    description="Remove one tag through id from tags model",
    response_model=None,
    status_code=204,
    dependencies=[Depends(current_superuser)]
)
async def delete_tag(tag_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Tag).where(tag_id == Tag.id)
    result = await session.execute(query)
    tag = result.scalars().first()

    if not tag:
        raise ExceptionNotFound(message="Tag not found")

    stmt = delete(Tag).where(tag_id == Tag.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
