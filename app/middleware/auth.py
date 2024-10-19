"""
app.middleware.auth.py
"""

from fastapi import Request, HTTPException, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.user_service import UserService
from app.db import SessionLocal
from app.models.user import User

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id, password = token.split(":")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_name == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        hashed_password = UserService.hash_password(password, user_id)
        if user.password == hashed_password:
            return user
        raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        db.close()


async def auth_middleware(request: Request, call_next):
    if request.url.path == "/favicon.ico":
        return Response(status_code=204)

    public_paths = ["/docs", "/openapi.json"]
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    try:
        token = request.headers["Authorization"].split("Bearer ")[1]
        user_id, password = token.split(":")
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_name == user_id).first()
            if not user:
                return Response(status_code=401, content="Invalid credentials")

            hashed_password = UserService.hash_password(password, user_id)
            if user.password == hashed_password:
                request.state.current_user = user
            else:
                return Response(status_code=401, content="Invalid credentials")
        finally:
            db.close()
    except (KeyError, IndexError):
        return Response(status_code=401, content="Invalid authorization header")

    return await call_next(request)
