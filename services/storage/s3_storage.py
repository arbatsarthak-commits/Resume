import uuid
from typing import Optional
from config import Config
from services.storage.base import StorageService

class S3StorageService(StorageService):
    """AWS S3 storage service using boto3."""

    def __init__(self, bucket_name: str = None, region: str = None):
        self.bucket_name = bucket_name or Config.AWS_S3_BUCKET
        self.region = region or Config.AWS_REGION
        self._s3_client = None

    @property
    def client(self):
        if self._s3_client is None:
            import boto3
            self._s3_client = boto3.client("s3", region_name=self.region)
        return self._s3_client

    def save_file(self, file_bytes: bytes, filename: str, subfolder: str = "uploads") -> str:
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        file_key = f"{subfolder}/{uuid.uuid4().hex}_{filename}"
        
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=file_key,
            Body=file_bytes,
            ContentType="application/octet-stream"
        )
        return file_key

    def get_file(self, file_key: str) -> Optional[bytes]:
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=file_key)
            return response['Body'].read()
        except Exception:
            return None

    def delete_file(self, file_key: str) -> bool:
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except Exception:
            return False

    def get_file_url(self, file_key: str) -> str:
        try:
            # Generate presigned URL for private S3 access
            return self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=3600
            )
        except Exception:
            return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_key}"
