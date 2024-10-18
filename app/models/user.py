"""
app.models.user.py
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    password = Column(String)
    pub_key = Column(String)
    is_root = Column(Boolean, default=False)

    # Define relationship with Collection, using lazy loading
    collections = relationship("Collection", back_populates="user", lazy="select")
