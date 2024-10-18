"""
app.api.v2.collection.py
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.collection import (
    CollectionCreate,
    CollectionResponse,
    CollectionList,
    CollectionDrop,
)
from app.services.collection_service import CollectionService
from app.db import get_db
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/list", response_model=CollectionList)
async def list_collections(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    collections = await CollectionService.list_collections(db, current_user)
    return CollectionList(code=0, data=[c.name for c in collections])


@router.post("/create", response_model=CollectionResponse)
async def create_collection(
    collection: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_collection = await CollectionService.create_collection(
        db, collection, current_user
    )
    if db_collection:
        return CollectionResponse(code=0, data={})
    raise HTTPException(status_code=400, detail="Failed to create collection")


@router.post("/drop", response_model=CollectionResponse)
async def drop_collection(
    collection: CollectionDrop,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_collection = await CollectionService.drop_collection(
        db, collection.name, current_user
    )
    if db_collection:
        return CollectionResponse(code=0, data={})
    raise HTTPException(status_code=404, detail="Collection not found")
