"""
app.services.collection_service.py
"""

from sqlalchemy.orm import Session
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate
from app.models.user import User


class CollectionService:
    @staticmethod
    async def list_collections(db: Session, current_user: User):
        return db.query(Collection).filter(Collection.user_id == current_user.id).all()

    @staticmethod
    async def create_collection(
        db: Session, collection: CollectionCreate, current_user: User
    ):
        db_collection = Collection(
            name=collection.name,
            dimension=collection.dimension,
            user_id=current_user.id,
        )
        db.add(db_collection)
        db.commit()
        db.refresh(db_collection)

        return db_collection

    @staticmethod
    async def drop_collection(db: Session, name: str, current_user: User):
        db_collection = (
            db.query(Collection)
            .filter(Collection.name == name, Collection.user_id == current_user.id)
            .first()
        )
        if db_collection:
            db.delete(db_collection)
            db.commit()

        return db_collection

    @staticmethod
    async def get_collection(db: Session, name: str, current_user: User):
        return (
            db.query(Collection)
            .filter(Collection.name == name, Collection.user_id == current_user.id)
            .first()
        )
