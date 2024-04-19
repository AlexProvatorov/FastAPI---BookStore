from fastapi import APIRouter

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/")
async def get_books():
    return


@router.post("/")
async def get_books():
    return


@router.patch("/")
async def get_books():
    return


@router.delete("/")
async def get_books():
    return


