from typing import Optional

from pydantic import BaseModel


class UserAccountBodyIn(BaseModel):
    user_account_id: str
    auth_type: Optional[int] = None


class UserAccountPutBodyIn(BaseModel):
    auth_type: int


class GetUserAccountOut(BaseModel):
    user_account_id: str
    auth_type: int
    report_id: str


class PostUserAccountOut(BaseModel):
    report_id: str


class PutUserAccountOut(BaseModel):
    report_id: str


class DeleteUserAccountOut(BaseModel):
    report_id: str
