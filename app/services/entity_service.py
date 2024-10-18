"""
app.services.entity_service.py
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
import numpy as np

from app.models.entity import Entity
from app.schemas.entity import EntityCreate, EntitySearch
from app.models.user import User
from app.services.collection_service import CollectionService


class EntityService:
    @staticmethod
    async def insert_entities(
        db: Session, entity_create: EntityCreate, current_user: User
    ):
        collection = await CollectionService.get_collection(
            db, entity_create.collection_name, current_user
        )
        if not collection:
            raise HTTPException(
                status_code=404, detail="Collection not found or you don't have access"
            )

        inserted_ids = []
        for item in entity_create.data:
            entity = Entity(
                collection_id=collection.id, vector=item["vector"], metadata=item
            )
            db.add(entity)
            db.flush()
            inserted_ids.append(entity.id)
        db.commit()
        return inserted_ids

    @staticmethod
    async def search_entities(db: Session, search: EntitySearch, current_user: User):
        collection = await CollectionService.get_collection(
            db, search.collection_name, current_user
        )
        if not collection:
            raise HTTPException(
                status_code=404, detail="Collection not found or you don't have access"
            )

        entities = db.query(Entity).filter(Entity.collection_id == collection.id).all()
        query_vector = np.array(search.data[0])

        results = []
        for entity in entities:
            entity_vector = np.array(entity.vector)
            distance = np.linalg.norm(query_vector - entity_vector)
            results.append(
                {
                    "id": entity.id,
                    "distance": float(distance),
                    "metadata": {
                        field: entity.metadata_ for field in search.output_fields
                    },
                }
            )

        results.sort(key=lambda x: x["distance"])
        return results[: search.limit]
