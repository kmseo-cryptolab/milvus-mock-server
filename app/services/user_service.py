"""
app.services.user_service.py
"""

import base64

from hashlib import pbkdf2_hmac
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserDrop


class UserService:
    @staticmethod
    def hash_password(password: str, username: str) -> str:
        salt = username.encode("utf-8")
        hashed = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return base64.b64encode(hashed).decode("utf-8")

    @staticmethod
    async def list_users(db: Session, current_user: User):
        if not current_user.is_root:
            raise HTTPException(status_code=403, detail="Only root can show user lists")
        return db.query(User).all()

    @staticmethod
    async def create_user(db: Session, user: UserCreate, current_user: User):
        if not current_user.is_root:
            raise HTTPException(status_code=403, detail="Only root can create users")

        existing_user = db.query(User).filter(User.user_name == user.user_name).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail={"code": 0, "message": "User already exists."}
            )

        hashed_password = UserService.hash_password(user.password, user.user_name)

        db_user = User(
            user_name=user.user_name, password=hashed_password, pub_key=user.pub_key
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def drop_user(db: Session, user: UserDrop, current_user: User):
        if not current_user.is_root:
            raise HTTPException(status_code=403, detail="Only root can drop users")

        db_user = db.query(User).filter(User.user_name == user.user_name).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(db_user)
        db.commit()
        return True
