from flask import Blueprint, request, jsonify, g

from services.auth.auth_service import (
    register_user, login_user, get_user_profile,
    update_user_profile, change_password, delete_user_account, decode_token
)
from middleware.auth_middleware import jwt_required, optional_auth, get_token_from_request

auth_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user account."""
    data = request.get_json() or {}
    email = data.get("email", "")
    password = data.get("password", "")
    full_name = data.get("full_name", "")

    try:
        result = register_user(email, password, full_name)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json() or {}
    email = data.get("email", "")
    password = data.get("password", "")

    try:
        result = login_user(email, password)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 401


@auth_bp.route("/profile", methods=["GET"])
@jwt_required
def profile():
    """Get current authenticated user's profile."""
    user_id = g.current_user["user_id"]
    profile_data = get_user_profile(user_id)

    if not profile_data:
        return jsonify({"success": False, "error": "User not found."}), 404

    return jsonify({"success": True, "user": profile_data}), 200


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required
def update_profile():
    """Update current user's profile."""
    user_id = g.current_user["user_id"]
    data = request.get_json() or {}

    try:
        updated = update_user_profile(user_id, data)
        return jsonify({"success": True, "user": updated}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required
def change_user_password():
    """Change authenticated user's password."""
    user_id = g.current_user["user_id"]
    data = request.get_json() or {}
    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    try:
        change_password(user_id, current_password, new_password)
        return jsonify({"success": True, "message": "Password changed successfully."}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@auth_bp.route("/delete-account", methods=["POST"])
@jwt_required
def delete_account():
    """Delete authenticated user's account and all associated data."""
    user_id = g.current_user["user_id"]
    data = request.get_json() or {}
    password = data.get("password", "")

    try:
        delete_user_account(user_id, password)
        return jsonify({"success": True, "message": "Account deleted successfully."}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@auth_bp.route("/verify", methods=["GET"])
@optional_auth
def verify_token():
    """Verify if the current token is valid."""
    current_user = g.current_user
    if current_user:
        return jsonify({
            "success": True,
            "authenticated": True,
            "user": {
                "user_id": current_user["user_id"],
                "email": current_user["email"],
                "role": current_user["role"]
            }
        }), 200

    return jsonify({"success": True, "authenticated": False}), 200

