import sqlite3
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any

from config import Config


class UserRepository(ABC):
    """Abstract interface for user data storage."""

    @abstractmethod
    def save_user(self, user_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        pass


class SQLiteUserRepository(UserRepository):
    """SQLite implementation of UserRepository for local mode."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_user(self, user_data: Dict[str, Any]) -> str:
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO users (user_id, email, password_hash, full_name, role, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    email=excluded.email,
                    password_hash=excluded.password_hash,
                    full_name=excluded.full_name,
                    role=excluded.role,
                    updated_at=excluded.updated_at
            """, (
                user_data["user_id"],
                user_data["email"],
                user_data["password_hash"],
                user_data["full_name"],
                user_data.get("role", "user"),
                user_data["created_at"],
                user_data["updated_at"]
            ))
            conn.commit()
        return user_data["user_id"]

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower(),))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        fields = []
        values = []
        for key, val in updates.items():
            fields.append(f"{key} = ?")
            values.append(val)

        if not fields:
            return False

        values.append(user_id)
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?",
                values
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_user(self, user_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0


class DynamoDBUserRepository(UserRepository):
    """DynamoDB implementation of UserRepository for AWS mode."""

    def __init__(self, table_name: str = None, region: str = None):
        self.table_name = table_name or f"{Config.AWS_DYNAMODB_TABLE}-users"
        self.region = region or Config.AWS_REGION
        self._dynamodb_resource = None

    @property
    def table(self):
        if self._dynamodb_resource is None:
            import boto3
            self._dynamodb_resource = boto3.resource("dynamodb", region_name=self.region)
        return self._dynamodb_resource.Table(self.table_name)

    def save_user(self, user_data: Dict[str, Any]) -> str:
        item = {
            "user_id": user_data["user_id"],
            "email": user_data["email"],
            "password_hash": user_data["password_hash"],
            "full_name": user_data["full_name"],
            "role": user_data.get("role", "user"),
            "created_at": user_data["created_at"],
            "updated_at": user_data["updated_at"]
        }
        self.table.put_item(Item=item)
        return user_data["user_id"]

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.get_item(Key={"user_id": user_id})
            return response.get("Item")
        except Exception:
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        try:
            from boto3.dynamodb.conditions import Attr
            response = self.table.scan(
                FilterExpression=Attr("email").eq(email.lower()),
                Limit=1
            )
            items = response.get("Items", [])
            return items[0] if items else None
        except Exception:
            return None

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        try:
            update_expr = "SET "
            expr_attrs = {}
            for i, (key, val) in enumerate(updates.items()):
                if i > 0:
                    update_expr += ", "
                update_expr += f"#{key} = :val{i}"
                expr_attrs[f"#key{i}"] = key
                expr_attrs[f":val{i}"] = val

            self.table.update_item(
                Key={"user_id": user_id},
                UpdateExpression=update_expr,
                ExpressionAttributeNames={f"#k{i}": k for i, k in enumerate(updates.keys())},
                ExpressionAttributeValues={f":v{i}": v for i, v in enumerate(updates.values())}
            )
            return True
        except Exception:
            return False

    def delete_user(self, user_id: str) -> bool:
        try:
            self.table.delete_item(Key={"user_id": user_id})
            return True
        except Exception:
            return False

