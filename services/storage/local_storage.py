import os
import uuid
from typing import Optional
from config import Config
from services.storage.base import StorageService

class LocalStorageService(StorageService):
    """Local filesystem storage service."""

    def __init__(self, upload_folder: str = None, generated_folder: str = None):
        self.upload_folder = upload_folder or Config.UPLOAD_FOLDER
        self.generated_folder = generated_folder or Config.GENERATED_FOLDER
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.generated_folder, exist_ok=True)

    def _get_target_dir(self, subfolder: str) -> str:
        if subfolder == "generated":
            return self.generated_folder
        return self.upload_folder

    def save_file(self, file_bytes: bytes, filename: str, subfolder: str = "uploads") -> str:
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        unique_name = f"{uuid.uuid4().hex}_{filename}" if filename else f"{uuid.uuid4().hex}.{ext}"
        target_dir = self._get_target_dir(subfolder)
        file_path = os.path.join(target_dir, unique_name)
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # Storage key is relative format: subfolder/unique_name
        return f"{subfolder}/{unique_name}"

    def get_file(self, file_key: str) -> Optional[bytes]:
        full_path = self._resolve_path(file_key)
        if not full_path or not os.path.exists(full_path):
            return None
        with open(full_path, "rb") as f:
            return f.read()

    def delete_file(self, file_key: str) -> bool:
        full_path = self._resolve_path(file_key)
        if full_path and os.path.exists(full_path):
            try:
                os.remove(full_path)
                return True
            except OSError:
                return False
        return False

    def get_file_url(self, file_key: str) -> str:
        return f"/api/files/{file_key}"

    def _resolve_path(self, file_key: str) -> Optional[str]:
        if file_key.startswith("generated/"):
            rel_path = file_key[len("generated/"):]
            return os.path.join(self.generated_folder, rel_path)
        elif file_key.startswith("uploads/"):
            rel_path = file_key[len("uploads/"):]
            return os.path.join(self.upload_folder, rel_path)
        else:
            # Fallback to upload folder
            return os.path.join(self.upload_folder, os.path.basename(file_key))
