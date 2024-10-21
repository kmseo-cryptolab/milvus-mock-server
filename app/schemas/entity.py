"""
app.schemas.entity.py
"""

from typing import List, Dict, Any

from .base import BaseSchema


class EntityCreate(BaseSchema):
    collection_name: str
    data: List[dict]


class EntitySearch(BaseSchema):
    collection_name: str
    data: List[List[float]]
    limit: int
    anns_field: str
    output_fields: List[str]


class EntitySearchResult(BaseSchema):
    id: int
    distance: float
    color: str


class EntitySearchResponse(BaseSchema):
    code: int
    data: List[Dict[str, Any]]
    """
    id: int
    distance: float
    **kwargs
    """


class EntityInsertResponse(BaseSchema):
    code: int
    data: Dict[str, Any]
