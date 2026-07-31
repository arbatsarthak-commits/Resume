import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "resumeiq-default-secret-key-12345")
    APP_ENV = os.environ.get("APP_ENV", "development")
    
    # Execution Mode: "local" or "aws"
    STORAGE_MODE = os.environ.get("STORAGE_MODE", "local").lower()
    DATABASE_MODE = os.environ.get("DATABASE_MODE", "sqlite").lower()
    
    # Local Storage Settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.environ.get("UPLOAD_FOLDER", "storage/uploads"))
    GENERATED_FOLDER = os.path.join(BASE_DIR, os.environ.get("GENERATED_FOLDER", "storage/generated"))
    DATABASE_PATH = os.path.join(BASE_DIR, os.environ.get("DATABASE_PATH", "data/resumeiq.db"))
    
    # JWT & Auth Settings
    JWT_SECRET = os.environ.get("JWT_SECRET", "resumeiq-jwt-secret-key-change-in-production")
    JWT_EXPIRY_HOURS = int(os.environ.get("JWT_EXPIRY_HOURS", "24"))
    
    # OpenAI (Optional - AI Enhancement)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Limits
    MAX_UPLOAD_SIZE_MB = int(os.environ.get("MAX_UPLOAD_SIZE_MB", "5"))
    MAX_CONTENT_LENGTH = MAX_UPLOAD_SIZE_MB * 1024 * 1024  # Flask upload limit in bytes
    ALLOWED_EXTENSIONS = {"pdf", "docx"}
    
    # AWS Settings (Optional in Local Mode)
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET", "resumeiq-uploads-bucket")
    AWS_DYNAMODB_TABLE = os.environ.get("AWS_DYNAMODB_TABLE", "resumeiq-analyses")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

    @classmethod
    def init_app(cls):
        """Ensure necessary local directories exist."""
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.GENERATED_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(cls.DATABASE_PATH), exist_ok=True)
