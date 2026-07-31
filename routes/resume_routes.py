from flask import Blueprint, send_file, jsonify
import io
from services.storage import get_storage_service

file_bp = Blueprint("file_api", __name__, url_prefix="/api")

@file_bp.route("/files/<path:file_key>", methods=["GET"])
def get_file(file_key):
    storage_svc = get_storage_service()
    file_bytes = storage_svc.get_file(file_key)
    if not file_bytes:
        return jsonify({"success": False, "error": "File not found."}), 404

    filename = file_key.rsplit('/', 1)[-1]
    mimetype = "application/pdf" if file_key.endswith(".pdf") else "application/octet-stream"
    if file_key.endswith(".docx"):
        mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return send_file(
        io.BytesIO(file_bytes),
        mimetype=mimetype,
        as_attachment=False,
        download_name=filename
    )
