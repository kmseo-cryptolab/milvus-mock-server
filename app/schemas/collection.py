"""
app.schemas.collection.py
"""

from typing import List

from .base import BaseSchema


class CollectionCreate(BaseSchema):
    name: str
    dimension: int


class CollectionResponse(BaseSchema):
    code: int
    data: dict


class CollectionList(BaseSchema):
    code: int
    data: List[str]


class CollectionDrop(BaseSchema):
    name: str
