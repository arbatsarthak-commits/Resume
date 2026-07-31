from flask import Blueprint, request, jsonify, send_file
import io
from core.resume_builder_pdf import generate_resume_pdf
from services.storage import get_storage_service

builder_bp = Blueprint("builder_api", __name__, url_prefix="/api")

@builder_bp.route("/resumes/build", methods=["POST"])
def build_resume():
    data = request.get_json() or {}
    template_id = data.get("template_id", "minimal_ats")

    personal = data.get("personal", {})
    if not personal.get("full_name"):
        return jsonify({"success": False, "error": "Full Name is required to build a resume."}), 400

    try:
        pdf_bytes = generate_resume_pdf(data, template_id=template_id)
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to generate PDF: {str(e)}"}), 500

    # Save to storage service
    storage_svc = get_storage_service()
    sanitized_name = "".join(c for c in personal.get("full_name") if c.isalnum() or c in (' ', '_', '-')).strip()
    filename = f"{sanitized_name.replace(' ', '_')}_Resume.pdf"
    file_key = storage_svc.save_file(pdf_bytes, filename, subfolder="generated")

    if request.args.get("download") == "true":
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename
        )

    return jsonify({
        "success": True,
        "file_key": file_key,
        "filename": filename,
        "download_url": f"/api/resumes/download?file_key={file_key}"
    }), 200

@builder_bp.route("/resumes/download", methods=["GET"])
def download_resume():
    file_key = request.args.get("file_key")
    if not file_key:
        return jsonify({"success": False, "error": "file_key parameter required."}), 400

    storage_svc = get_storage_service()
    file_bytes = storage_svc.get_file(file_key)
    if not file_bytes:
        return jsonify({"success": False, "error": "Requested resume file was not found."}), 404

    filename = file_key.rsplit('/', 1)[-1]
    return send_file(
        io.BytesIO(file_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename
    )
