"""
app.schemas.user.py
"""

from typing import List

from .base import BaseSchema


class UserCreate(BaseSchema):
    user_name: str
    password: str
    pub_key: str


class UserDrop(BaseSchema):
    user_name: str


class UserResponse(BaseSchema):
    code: int
    data: dict


class UserList(BaseSchema):
    code: int
    data: List[str]


class User(BaseSchema):
    id: int
    user_name: str
    pub_key: str
