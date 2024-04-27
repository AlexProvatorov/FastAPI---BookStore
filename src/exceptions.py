class ExceptionBookstore(Exception):
    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        self.details = message


class ExceptionBadRequest(ExceptionBookstore):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class ExceptionForbidden(ExceptionBookstore):
    def __init__(self, message: str):
        super().__init__(message, status_code=403)


class ExceptionNotFound(ExceptionBookstore):
    def __init__(self, message: str):
        super().__init__(message, status_code=404)
