"""
app.api.v2.entity.py
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.entity import (
    EntityCreate,
    EntitySearch,
    EntitySearchResponse,
    EntityInsertResponse,
)
from app.services.entity_service import EntityService
from app.db import get_db
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/search", response_model=EntitySearchResponse)
async def search_vectors(
    search: EntitySearch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Vector를 유사도 기반으로 조회합니다.

    See API Spec at [Milvus API(V2)::Vector Search](https://milvus.io/api-reference/restful/v2.4.x/v2/Vector%20(v2)/Search.md)
    """
    results = await EntityService.search_entities(db, search, current_user)
    return EntitySearchResponse(code=0, data=results)


@router.post("/insert", response_model=EntityInsertResponse)
async def insert_vectors(
    entity_create: EntityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Vector를 입력합니다.

    See API Spec at [Milvus API(V2)::Vector Insert](https://milvus.io/api-reference/restful/v2.4.x/v2/Vector%20(v2)/Insert.md)
    """
    inserted_ids = await EntityService.insert_entities(db, entity_create, current_user)
    if inserted_ids:
        return EntityInsertResponse(
            code=0, data={"insertCount": len(inserted_ids), "insertIds": inserted_ids}
        )
    raise HTTPException(status_code=400, detail="Failed to insert entities")
