from typing import List

from pydantic import BaseModel


class TenantMetadata(BaseModel):
    tenant_id: str
    collections: List[str]
