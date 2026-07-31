from config import Config
from services.database.base import AnalysisRepository
from services.database.sqlite_repository import SQLiteAnalysisRepository
from services.database.dynamodb_repository import DynamoDBAnalysisRepository
from services.database.user_repository import SQLiteUserRepository, DynamoDBUserRepository, UserRepository

def get_analysis_repository() -> AnalysisRepository:
    """Factory function returning the configured AnalysisRepository implementation."""
    if Config.DATABASE_MODE == "dynamodb":
        return DynamoDBAnalysisRepository()
    return SQLiteAnalysisRepository()

def get_user_repository() -> UserRepository:
    """Factory function returning the configured UserRepository implementation."""
    if Config.DATABASE_MODE == "dynamodb":
        return DynamoDBUserRepository()
    return SQLiteUserRepository()
