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
    async def insert_entities(db: Session, entity_create: EntityCreate, current_user: User):
        collection = await CollectionService.get_collection(
            db, entity_create.collection_name, current_user
        )
        if not collection:
            raise HTTPException(
                status_code=404, detail="Collection not found or you don't have access"
            )

        inserted_ids = []

        for item in entity_create.data:
            entity = Entity(collection_id=collection.id, data=item)
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

        # query_vector가 768차원이 아니면 zero padding
        if query_vector.shape[0] < collection.dimension:
            padding_length = collection.dimension - query_vector.shape[0]
            query_vector = np.pad(query_vector, (0, padding_length), mode="constant")

        anns_field = search.anns_field
        output_fields = search.output_fields

        # anns_field의 데이터가 List[float]인지 첫 번째 entity로 체크
        if entities:
            first_vector = entities[0].data.get(anns_field)
            if not isinstance(first_vector, list) or not all(
                isinstance(x, float) for x in first_vector
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"The anns_field '{anns_field}' must be a list of floats.",
                )

        results = []
        # 거리 계산 및 결과 저장
        for entity in entities:
            vector = entity.data.get(anns_field)
            entity_vector = np.array(vector)

            # cosine similarity 계산
            dot_product = np.dot(query_vector, entity_vector)
            norm_query = np.linalg.norm(query_vector)
            norm_entity = np.linalg.norm(entity_vector)
            cosine_similarity = dot_product / (norm_query * norm_entity)

            # output_fields에서 필드가 존재하는 경우에만 추가
            result_data = {
                field: entity.data[field] for field in output_fields if field in entity.data
            }
            results.append(
                {
                    "id": entity.id,
                    "distance": 1 - cosine_similarity,  # cosine similarity를 distance로 변환
                    **result_data,
                }
            )

        # 거리 기준으로 정렬 후 제한된 개수 반환
        results.sort(key=lambda x: x["distance"])
        return results[: search.limit]
