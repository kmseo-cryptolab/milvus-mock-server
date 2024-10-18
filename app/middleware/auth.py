"""
app.middleware.auth.py
"""

from fastapi import Request, HTTPException, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db import SessionLocal
from app.models.user import User

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id, password = token.split(":")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_name == user_id).first()

        if user and user.password == password:
            return user
        raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        db.close()


async def auth_middleware(request: Request, call_next):
    # Handle favicon requests
    if request.url.path == "/favicon.ico":
        return Response(status_code=204)  # No Content

    # Bypass authentication for certain paths
    public_paths = [
        "/docs",
        "/openapi.json",  # Swagger and OpenAPI spec
    ]
    if any(request.url.path.startswith(path) for path in public_paths):
        response = await call_next(request)
        return response

    # Authenticate for other paths
    try:
        token = request.headers["Authorization"].split("Bearer ")[1]
        user_id, password = token.split(":")
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_name == user_id).first()
            if (
                user and user.password == password
            ):  # In production, use proper password hashing
                request.state.current_user = user
            else:
                # Return 401 Unauthorized for invalid credentials
                return Response(status_code=401, content="Invalid credentials")
        finally:
            db.close()
    except (KeyError, IndexError):
        # Return 401 Unauthorized for invalid authorization header or missing keys
        return Response(status_code=401, content="Invalid authorization header")

    response = await call_next(request)
    return response
