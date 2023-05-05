from fastapi import APIRouter, Path, Body, Query
from typing import List
from boto3.dynamodb.conditions import Attr

from app.service.log import ValidationErrorLoggingRoute
from app.model.dynamodb import DDB_TABLE
from app.schema.user.account import (
    UserAccountBodyIn,
    UserAccountPutBodyIn,
    GetUserAccountOut,
    PostUserAccountOut,
    PutUserAccountOut,
    DeleteUserAccountOut
)
from app.service.exception import CustomException

router = APIRouter(route_class=ValidationErrorLoggingRoute)


@router.get("/{user_id}", description="유저 정보 조회", tags=["user"], response_model=List[GetUserAccountOut])
async def get_user(user_id: str = Path(..., description="유저 아이디")):
    response = DDB_TABLE.scan(FilterExpression=Attr('user_id').eq(user_id))

    if len(response['Items']) == 0:
        return []

    return response['Items']


@router.post("/{user_id}", description="신규 유저 정보 입력", tags=["user"], response_model=PostUserAccountOut)
async def post_user(user_id: str = Path(..., description="유저 아이디"),
                    body: List[UserAccountBodyIn] = Body(..., description="Dynamodb Body")):
    for user_account in body:
        DDB_TABLE.put_item(Item=user_account.dict())

    return {'user_id': user_id}


@router.put("/{user_id}", description="유저 정보 수정", tags=["user"], response_model=PutUserAccountOut)
async def put_user(user_id: str = Path(..., description="유저 아이디"),
                   body: UserAccountPutBodyIn = Body(..., description="Dynamodb Body")):
    response = DDB_TABLE.scan(FilterExpression=Attr('user_id').eq(user_id))

    if len(response['Items']) == 0:
        raise CustomException(400, {'message': 'The user does not exist'})

    DDB_TABLE.put_item(Item=body.dict())

    return {'user_id': user_id}


@router.delete("/{user_id}", description="유저 정보 삭제", tags=["user"], response_model=DeleteUserAccountOut)
async def delete_user(user_id: str = Path(..., description="유저 아이디")):
    DDB_TABLE.delete_item(user_id={'user_id': user_id})

    return {'user_id': user_id}
