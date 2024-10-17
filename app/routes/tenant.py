from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.tenant import get_tenant, TenantNotFoundError

tenant_router = APIRouter()


@tenant_router.get("/tenants/{tenant_id}")
async def serve_tenant(tenant_id: str):
    """
    Serve tenant data based on tenant ID
    """
    try:
        tenant = get_tenant(tenant_id=tenant_id)
    except TenantNotFoundError as e:
        return JSONResponse(
            status_code=404, content={"response": "Error", "detail": str(e)}
        )

    return {"response": "OK", "tenant": tenant}
