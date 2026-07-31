import functools
from typing import Optional, Callable

from flask import request, jsonify, g

from services.auth.auth_service import decode_token


def get_token_from_request() -> Optional[str]:
    """Extract JWT token from Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None


def jwt_required(f: Callable) -> Callable:
    """Decorator that requires a valid JWT token for route access."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if not token:
            return jsonify({"success": False, "error": "Authentication required. Please provide a valid token."}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({"success": False, "error": "Invalid or expired token. Please login again."}), 401

        # Store user info in Flask global context
        g.current_user = {
            "user_id": payload["sub"],
            "email": payload["email"],
            "role": payload.get("role", "user")
        }

        return f(*args, **kwargs)

    return decorated


def optional_auth(f: Callable) -> Callable:
    """Decorator that optionally extracts user info from token if present."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        g.current_user = None

        if token:
            payload = decode_token(token)
            if payload:
                g.current_user = {
                    "user_id": payload["sub"],
                    "email": payload["email"],
                    "role": payload.get("role", "user")
                }

        return f(*args, **kwargs)

    return decorated


def admin_required(f: Callable) -> Callable:
    """Decorator that requires admin role."""
    @functools.wraps(f)
    @jwt_required
    def decorated(*args, **kwargs):
        if g.current_user.get("role") != "admin":
            return jsonify({"success": False, "error": "Admin access required."}), 403
        return f(*args, **kwargs)

    return decorated

