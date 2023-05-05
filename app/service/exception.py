from fastapi.exceptions import HTTPException


class CustomException(HTTPException):
    def __str__(self):
        return f"status_code={self.status_code}, message={self.detail}"
