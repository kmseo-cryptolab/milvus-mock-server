"""
app.models.entity.py
"""

from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id"))
    data = Column(JSON)  # data = Column(JSON)

    # Relationship with Collection, using lazy loading
    collection = relationship("Collection", back_populates="entities", lazy="select")
