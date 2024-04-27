from fastapi import Request
from starlette.responses import JSONResponse

from exceptions import ExceptionBookstore


def handle_exception_bookstore(request: Request, exception: ExceptionBookstore):
    return JSONResponse(status_code=exception.status_code, content={
        "error": {
            "details": exception.details,
        }
    }
    )
