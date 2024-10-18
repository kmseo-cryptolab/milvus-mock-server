"""
app.api.v2.user.py
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserDrop, UserResponse, UserList
from app.services.user_service import UserService
from app.db import get_db
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/list", response_model=UserList)
async def list_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> UserList:

    users: List[User]

    try:
        users = await UserService.list_users(db, current_user)

    except HTTPException as e:
        raise e

    return UserList(code=0, data=[u.user_name for u in users])


@router.post("/create", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await UserService.create_user(db, user, current_user)

    except HTTPException as e:
        raise e

    return UserResponse(code=0, data={})


@router.post("/drop", response_model=UserResponse)
async def drop_user(
    user_name: UserDrop,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await UserService.drop_user(db, user_name, current_user)

    except HTTPException as e:
        raise e

    return UserResponse(code=0, data={})
