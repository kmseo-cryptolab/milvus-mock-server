from abc import ABC, abstractmethod
from typing import Any


class BaseStorageManager(ABC):

    @abstractmethod
    def __init__(self, tenant_id: str) -> None:
        """
        Initialize the storage manager for a specific tenant.

        :param tenant_id: The unique identifier for the tenant.
        """
        raise NotImplementedError()

    @abstractmethod
    def load_tenant_metadata(self, tenant_id: str) -> dict:
        """
        Load metadata for a specific tenant.

        :param tenant_id: The unique identifier for the tenant.
        :return: A dictionary containing the tenant's metadata.
        """
        raise NotImplementedError()

    @abstractmethod
    def load_object(self, tenant_id: str, object_name: str) -> Any:
        """
        Load an object for a specific tenant.

        :param tenant_id: The unique identifier for the tenant.
        :param object_name: The name or identifier of the object to load.
        :return: The loaded object.
        """
        raise NotImplementedError()
