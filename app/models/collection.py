"""
app.models.collection.py
"""

from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    dimension = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    metadata_ = Column("metadata", JSON)  # metadata = Column(JSON)

    # Relationship with User, using lazy loading
    user = relationship("User", back_populates="collections", lazy="select")

    # Relationship with Entity, using lazy loading
    entities = relationship("Entity", back_populates="collection", lazy="select")
