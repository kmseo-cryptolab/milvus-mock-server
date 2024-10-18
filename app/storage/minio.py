import os
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
import json
from base import BaseStorageManager

# Load environment variables
load_dotenv()


class MinioStorageManager(BaseStorageManager):

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.minio_client = Minio(
            os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=os.getenv("MINIO_SECURE", "True").lower() == "true",
        )
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME")

    def load_tenant_metadata(self, tenant_id: str) -> dict:
        try:
            response = self.minio_client.get_object(
                self.bucket_name, f"{tenant_id}/metadata.json"
            )
            return json.loads(response.read().decode("utf-8"))

        except S3Error as e:
            if e.code == "NoSuchKey":
                raise ValueError(f"Metadata for tenant {tenant_id} not found")
            else:
                raise

    def load_object(self, tenant_id: str, object_name: str) -> bytes:
        try:
            response = self.minio_client.get_object(
                self.bucket_name, f"{tenant_id}/{object_name}"
            )
            return response.read()

        except S3Error as e:
            if e.code == "NoSuchKey":
                raise ValueError(
                    f"Object {object_name} for tenant {tenant_id} not found"
                )
            else:
                raise
