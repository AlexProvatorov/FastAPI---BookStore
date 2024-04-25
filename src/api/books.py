from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.sql import exists
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from db.models.goods import Book, Tag, Author, TagOfBooks, AuthorOfBooks
from apps.goods.schemas import TagOfBook as TagOfBookSchema
from apps.goods.schemas import AuthorOfBook as AuthorOfBookSchema


from apps.goods.schemas import BookCreate

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/")
async def get_books(session: AsyncSession = Depends(get_async_session)):
    query = select(Book)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{book_id}")
async def get_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Book).where(book_id == Book.id)
    result = await session.execute(query)
    result = result.scalars().all()
    return result


@router.post("/")
async def add_book(new_book: BookCreate, session: AsyncSession = Depends(get_async_session)):
    is_tags_exists = exists().where(Tag.id.in_(new_book.tags)).select()
    is_authors_exists = exists().where(Author.id.in_(new_book.authors)).select()
    is_tags_exists = (await session.execute(is_tags_exists)).scalar()
    is_authors_exists = (await session.execute(is_authors_exists)).scalar()

    if not is_tags_exists or not is_authors_exists:
        raise HTTPException(status_code=404, detail="Book not found")

    new_book = new_book.dict()
    list_tags = new_book.pop("tags")
    list_authors = new_book.pop("authors")
    stmt = insert(Book).values(new_book)
    cursor_exec = await session.execute(stmt)
    new_book_id = cursor_exec.returned_defaults[0]

    tags = [TagOfBookSchema(id_tag=id_tag, id_book=new_book_id).dict() for id_tag in list_tags]
    authors = [AuthorOfBookSchema(id_author=id_author, id_book=new_book_id).dict() for id_author in list_authors]

    stmt = insert(TagOfBooks).values(tags)
    await session.execute(stmt)

    stmt = insert(AuthorOfBooks).values(authors)
    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}


@router.patch("/{book_id}")
async def edit_book(book_id: int, new_book: BookCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Book).values(**new_book.dict()).where(book_id == Book.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete(
    path="/{book_id}",
    name="Delete book",
    description="Remove book from books list",
    status_code=204,
)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Book).where(book_id == Book.id)
    await session.execute(stmt)
    await session.commit()
