from fastapi import APIRouter


retrieval_router = APIRouter()


@retrieval_router.post("/retrieval")
async def retrieval() -> str:
    """
    [x] 1. index process
    [>] 2. retrieval process
    """
    return "OK"
