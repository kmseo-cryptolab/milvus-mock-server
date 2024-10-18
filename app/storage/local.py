import os
import json
from pathlib import Path
from base import BaseStorageManager


class LocalStorageManager(BaseStorageManager):
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.base_path = Path(os.getenv("LOCAL_STORAGE_PATH", "local_storage"))
        self.tenant_path = self.base_path / tenant_id
        self.tenant_path.mkdir(parents=True, exist_ok=True)

    def load_tenant_metadata(self, tenant_id: str) -> dict:
        metadata_path = self.tenant_path / "metadata.json"
        if not metadata_path.exists():
            raise ValueError(f"Metadata for tenant {tenant_id} not found")

        with open(metadata_path, "r") as f:
            return json.load(f)

    def load_object(self, tenant_id: str, object_name: str) -> bytes:
        object_path = self.tenant_path / object_name
        if not object_path.exists():
            raise ValueError(f"Object {object_name} for tenant {tenant_id} not found")

        with open(object_path, "rb") as f:
            return f.read()

    # Additional helper methods for debugging

    def save_tenant_metadata(self, tenant_id: str, metadata: dict) -> None:
        metadata_path = self.tenant_path / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

    def save_object(self, tenant_id: str, object_name: str, data: bytes) -> None:
        object_path = self.tenant_path / object_name
        with open(object_path, "wb") as f:
            f.write(data)

    def list_objects(self, tenant_id: str) -> list:
        return [f.name for f in self.tenant_path.iterdir() if f.is_file()]

    def delete_object(self, tenant_id: str, object_name: str) -> None:
        object_path = self.tenant_path / object_name
        if object_path.exists():
            object_path.unlink()
        else:
            raise ValueError(f"Object {object_name} for tenant {tenant_id} not found")
