"""
app.services.user_service.py
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserDrop


class UserService:

    @staticmethod
    async def list_users(db: Session, current_user: User):

        if not current_user.is_root:
            raise HTTPException(status_code=403, detail="Only root can show user lists")

        return db.query(User).all()

    @staticmethod
    async def create_user(db: Session, user: UserCreate, current_user: User):
        if not current_user.is_root:
            raise HTTPException(status_code=403, detail="Only root can create users")

        # Check for existing user with the same user_name
        existing_user = db.query(User).filter(User.user_name == user.user_name).first()
        if existing_user:
            # Return a specific message if the user already exists
            raise HTTPException(
                status_code=400, detail={"code": 0, "message": "User already exists."}
            )

        # Create a new user if no duplication is found
        db_user = User(
            user_name=user.user_name, password=user.password, pub_key=user.pub_key
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
