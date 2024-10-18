import os
from dotenv import load_dotenv
import boto3
import json

from botocore.exceptions import ClientError
from base import BaseStorageManager

# Load environment variables
load_dotenv()


class S3StorageManager(BaseStorageManager):

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )
        self.bucket_name = os.getenv("S3_BUCKET_NAME")

    def load_tenant_metadata(self, tenant_id: str) -> dict:
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name, Key=f"{tenant_id}/metadata.json"
            )
            return json.loads(response["Body"].read().decode("utf-8"))

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise ValueError(f"Metadata for tenant {tenant_id} not found")
            else:
                raise ClientError

    def load_object(self, tenant_id: str, object_name: str) -> bytes:
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name, Key=f"{tenant_id}/{object_name}"
            )
            return response["Body"].read()

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise ValueError(
                    f"Object {object_name} for tenant {tenant_id} not found"
                )
            else:
                raise ClientError
