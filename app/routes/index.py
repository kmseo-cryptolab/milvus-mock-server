from typing import List

from fastapi import APIRouter


index_router = APIRouter()


@index_router.post("/index")
async def index() -> List[str]:
    """
    [>] 1. index process
    [ ] 2. retrieval process
    """
    return ["OK"]
