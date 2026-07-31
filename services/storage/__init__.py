from config import Config
from services.storage.base import StorageService
from services.storage.local_storage import LocalStorageService
from services.storage.s3_storage import S3StorageService

def get_storage_service() -> StorageService:
    """Factory function returning the configured StorageService implementation."""
    if Config.STORAGE_MODE == "aws":
        return S3StorageService()
    return LocalStorageService()
