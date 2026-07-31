from abc import ABC, abstractmethod
from typing import Optional

class StorageService(ABC):
    """Abstract interface for file storage operations."""

    @abstractmethod
    def save_file(self, file_bytes: bytes, filename: str, subfolder: str = "uploads") -> str:
        """Saves a file and returns its storage key / relative path."""
        pass

    @abstractmethod
    def get_file(self, file_key: str) -> Optional[bytes]:
        """Retrieves raw file bytes by key."""
        pass

    @abstractmethod
    def delete_file(self, file_key: str) -> bool:
        """Deletes a file by key."""
        pass

    @abstractmethod
    def get_file_url(self, file_key: str) -> str:
        """Returns a URL or path to access the file."""
        pass
