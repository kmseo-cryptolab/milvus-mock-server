from app.storage import MinioStorageManager


class TenantNotFoundError(Exception):
    """Raised when a tenant is not found"""

    pass


def get_tenant(tenant_id: str) -> dict:
    """
    Serve tenant data based on tenant ID
    """
    # 실제 구현에서는 데이터베이스나 다른 저장소에서 tenant 정보를 조회해야 합니다.

    tenants = {
        "tenant-001": {"name": "Tenant 001", "description": "First tenant"},
        "tenant-002": {"name": "Tenant 002", "description": "Second tenant"},
    }
    if tenant_id not in tenants:
        raise TenantNotFoundError(f"Tenant with id {tenant_id} not found")

    return tenants[tenant_id]


"""
def get_tenant(tenant_id: str) -> dict:

    tenant: dict

    try:
        tenant = MinioStorageManager.load_tenant_metadata(tenant_id=tenant_id)

    except ClientError as e:
        raise TenantNotFoundError(f"Tenant with id {tenant_id} not found")
    
    return tenant
"""
