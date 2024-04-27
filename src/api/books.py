from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.sql import exists
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from db.models.goods import Book, Tag, Author, TagOfBooks, AuthorOfBooks
from apps.goods.schemas import TagOfBook as TagOfBookSchema
from apps.goods.schemas import AuthorOfBook as AuthorOfBookSchema


from apps.goods.schemas import BookCreate
from exceptions import ExceptionNotFound

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get(
    path="/",
    name="Get all books",
    description="Get all books from books model",
    status_code=200,
)
async def get_books(session: AsyncSession = Depends(get_async_session)):
    query = select(Book)
    result = await session.execute(query)
    books = result.scalars().all()

    if not books:
        raise ExceptionNotFound(message="Books not found")

    return books


@router.get(
    path="/{book_id}",
    name="Get one book",
    description="Get one book through id from books model",
    status_code=200,
)
async def get_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Book).where(book_id == Book.id)
    result = await session.execute(query)
    book = result.scalars().all()

    if not book:
        raise ExceptionNotFound(message="Book not found")

    return book


@router.post(
    path="/",
    name="Create new book",
    description="Create new book for books model",
    response_model=BookCreate,
    status_code=201,
)
async def add_book(
    new_book: BookCreate, session: AsyncSession = Depends(get_async_session)
):
    is_tags_exists = exists().where(Tag.id.in_(new_book.tags)).select()
    is_authors_exists = exists().where(Author.id.in_(new_book.authors)).select()
    is_tags_exists = (await session.execute(is_tags_exists)).scalar()
    is_authors_exists = (await session.execute(is_authors_exists)).scalar()

    if not is_tags_exists or not is_authors_exists:
        raise ExceptionNotFound(
            message="Book must contain at least one author and a tag"
        )

    book = new_book.dict()
    list_tags = book.pop("tags")
    list_authors = book.pop("authors")
    stmt = insert(Book).values(book)
    cursor_exec = await session.execute(stmt)
    new_book_id = cursor_exec.returned_defaults[0]

    tags = [
        TagOfBookSchema(id_tag=id_tag, id_book=new_book_id).dict()
        for id_tag in list_tags
    ]
    authors = [
        AuthorOfBookSchema(id_author=id_author, id_book=new_book_id).dict()
        for id_author in list_authors
    ]

    stmt = insert(TagOfBooks).values(tags)
    await session.execute(stmt)

    stmt = insert(AuthorOfBooks).values(authors)
    await session.execute(stmt)
    await session.commit()

    return new_book


@router.patch(
    path="/{book_id}",
    name="Change book",
    description="Change book for books model",
    response_model=BookCreate,
    status_code=201,
)
async def edit_book(
    book_id: int,
    changed_book: BookCreate,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Book).where(book_id == Book.id)
    result = await session.execute(query)
    book = result.scalars().first()

    if not book:
        raise ExceptionNotFound(message="Book not found")

    is_tags_exists = exists().where(Tag.id.in_(changed_book.tags)).select()
    is_authors_exists = exists().where(Author.id.in_(changed_book.authors)).select()
    is_tags_exists = (await session.execute(is_tags_exists)).scalar()
    is_authors_exists = (await session.execute(is_authors_exists)).scalar()

    if not is_tags_exists or not is_authors_exists:
        raise ExceptionNotFound(
            message="Book must contain at least one author and a tag"
        )

    book = changed_book.dict()
    list_tags = book.pop("tags")
    list_authors = book.pop("authors")
    stmt = update(Book).values(book).where(book_id == Book.id)
    await session.execute(stmt)

    tags = [
        TagOfBookSchema(id_tag=id_tag, id_book=book_id).dict() for id_tag in list_tags
    ]
    authors = [
        AuthorOfBookSchema(id_author=id_author, id_book=book_id).dict()
        for id_author in list_authors
    ]

    stmt = insert(TagOfBooks).values(tags)
    await session.execute(stmt)

    stmt = insert(AuthorOfBooks).values(authors)
    await session.execute(stmt)
    await session.commit()

    return changed_book


@router.delete(
    path="/{book_id}",
    name="Delete book",
    description="Remove book from books list",
    response_model=None,
    status_code=204,
)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Book).where(book_id == Book.id)
    result = await session.execute(query)
    book = result.scalars().first()

    if not book:
        raise ExceptionNotFound(message="Book not found")

    stmt = delete(Book).where(book_id == Book.id)
    await session.execute(stmt)
    await session.commit()
