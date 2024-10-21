"""
app.main.py
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from app.api.v2 import collection, entity, user
from app.db import engine, Base, SessionLocal
from app.models.user import User
from app.middleware.auth import auth_middleware


# Create root user
def create_root_user():
    db = SessionLocal()

    try:
        root_user = db.query(User).filter(User.user_name == "root").first()
        if not root_user:
            user_name = "root"
            password = "EVRs6qDsJRoo9rcKOvOBICNSfwa61ycyk8Rr+YWMgGA="  # hashed, iter=100000
            root_user = User(user_name=user_name, password=password, is_root=True)

            db.add(root_user)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup logic
    create_root_user()

    yield
    # Shutdown logic can be added here if needed


app = FastAPI(lifespan=lifespan)

# Add middleware
app.middleware("http")(auth_middleware)


# Exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# Create tables for all models
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router, prefix="/v2/vectordb/users", tags=["User (v2)"])
app.include_router(collection.router, prefix="/v2/vectordb/collections", tags=["Collection (v2)"])
app.include_router(entity.router, prefix="/v2/vectordb/entities", tags=["Entity (v2)"])
