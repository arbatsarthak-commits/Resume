import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

import bcrypt
import jwt

from config import Config
from services.database import get_user_repository


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def generate_token(user_id: str, email: str, role: str = "user") -> str:
    """Generate a JWT token for authenticated user."""
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRY_HOURS)
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify a JWT token. Returns payload or None if invalid."""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def register_user(email: str, password: str, full_name: str) -> Dict[str, Any]:
    """Register a new user. Returns user data or raises ValueError."""
    if not email or not email.strip():
        raise ValueError("Email is required.")
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")
    if not full_name or not full_name.strip():
        raise ValueError("Full name is required.")

    email = email.strip().lower()
    full_name = full_name.strip()

    repo = get_user_repository()

    # Check if user already exists
    existing = repo.get_user_by_email(email)
    if existing:
        raise ValueError("An account with this email already exists.")

    user_id = str(uuid.uuid4())
    hashed_pw = hash_password(password)
    created_at = datetime.utcnow().isoformat()

    user_data = {
        "user_id": user_id,
        "email": email,
        "password_hash": hashed_pw,
        "full_name": full_name,
        "role": "user",
        "created_at": created_at,
        "updated_at": created_at
    }

    repo.save_user(user_data)

    token = generate_token(user_id, email, role="user")

    return {
        "success": True,
        "user_id": user_id,
        "email": email,
        "full_name": full_name,
        "token": token
    }


def login_user(email: str, password: str) -> Dict[str, Any]:
    """Authenticate a user. Returns user data + token or raises ValueError."""
    if not email or not password:
        raise ValueError("Email and password are required.")

    email = email.strip().lower()

    repo = get_user_repository()
    user = repo.get_user_by_email(email)
    if not user:
        raise ValueError("Invalid email or password.")

    if not verify_password(password, user.get("password_hash", "")):
        raise ValueError("Invalid email or password.")

    token = generate_token(user["user_id"], user["email"], user.get("role", "user"))

    return {
        "success": True,
        "user_id": user["user_id"],
        "email": user["email"],
        "full_name": user.get("full_name", ""),
        "token": token
    }


def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user profile by ID (sensitive fields excluded)."""
    repo = get_user_repository()
    user = repo.get_user(user_id)
    if not user:
        return None

    # Return profile without password hash
    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "full_name": user.get("full_name", ""),
        "role": user.get("role", "user"),
        "created_at": user.get("created_at", ""),
        "updated_at": user.get("updated_at", "")
    }


def update_user_profile(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update user profile fields."""
    repo = get_user_repository()
    user = repo.get_user(user_id)
    if not user:
        raise ValueError("User not found.")

    allowed_fields = {"full_name"}
    filtered = {k: v for k, v in updates.items() if k in allowed_fields and v}
    if not filtered:
        raise ValueError("No valid fields to update.")

    filtered["updated_at"] = datetime.utcnow().isoformat()
    repo.update_user(user_id, filtered)

    return get_user_profile(user_id)


def change_password(user_id: str, current_password: str, new_password: str) -> bool:
    """Change user password after verifying current password."""
    repo = get_user_repository()
    user = repo.get_user(user_id)
    if not user:
        raise ValueError("User not found.")

    if not verify_password(current_password, user.get("password_hash", "")):
        raise ValueError("Current password is incorrect.")

    if len(new_password) < 6:
        raise ValueError("New password must be at least 6 characters.")

    new_hash = hash_password(new_password)
    repo.update_user(user_id, {
        "password_hash": new_hash,
        "updated_at": datetime.utcnow().isoformat()
    })

    return True


def delete_user_account(user_id: str, password: str) -> bool:
    """Delete user account and all associated data."""
    repo = get_user_repository()
    user = repo.get_user(user_id)
    if not user:
        raise ValueError("User not found.")

    if not verify_password(password, user.get("password_hash", "")):
        raise ValueError("Password is incorrect.")

    # Delete all user's analyses
    from services.database import get_analysis_repository
    from services.storage import get_storage_service

    analysis_repo = get_analysis_repository()
    storage_svc = get_storage_service()

    analyses = analysis_repo.list_analyses(user_id=user_id, limit=1000)
    for analysis in analyses:
        file_key = analysis.get("resume_file_key")
        if file_key:
            storage_svc.delete_file(file_key)
        analysis_repo.delete_analysis(analysis.get("analysis_id"))

    # Delete user
    repo.delete_user(user_id)

    return True

