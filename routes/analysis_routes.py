from flask import Blueprint, request, jsonify
from services.storage import get_storage_service
from services.database import get_analysis_repository
from core.resume_parser import process_resume_analysis
from config import Config

analysis_bp = Blueprint("analysis_api", __name__, url_prefix="/api")

@analysis_bp.route("/resumes/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return jsonify({"success": False, "error": "No resume file provided."}), 400

    file = request.files["resume"]
    if not file or file.filename == "":
        return jsonify({"success": False, "error": "Please select a valid PDF or DOCX file."}), 400

    filename = file.filename
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in Config.ALLOWED_EXTENSIONS:
        return jsonify({"success": False, "error": "Invalid file format. Only PDF and DOCX files are allowed."}), 400

    file_bytes = file.read()
    if len(file_bytes) == 0:
        return jsonify({"success": False, "error": "The uploaded file is empty."}), 400

    if len(file_bytes) > Config.MAX_CONTENT_LENGTH:
        return jsonify({"success": False, "error": f"File size exceeds limit of {Config.MAX_UPLOAD_SIZE_MB}MB."}), 400

    jd_text = request.form.get("job_description")

    # 1. Save uploaded file to storage service (local or S3)
    storage_svc = get_storage_service()
    resume_file_key = storage_svc.save_file(file_bytes, filename, subfolder="uploads")

    # 2. Run deterministic ATS analysis
    try:
        result = process_resume_analysis(
            file_bytes=file_bytes,
            filename=filename,
            jd_text=jd_text,
            resume_file_key=resume_file_key
        )
    except ValueError as ve:
        # Delete file if parsing failed
        storage_svc.delete_file(resume_file_key)
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        storage_svc.delete_file(resume_file_key)
        return jsonify({"success": False, "error": "Analysis could not be completed. Please check your document and try again."}), 500

    # 3. Store result in repository (SQLite or DynamoDB)
    db_repo = get_analysis_repository()
    db_repo.save_analysis(result)

    return jsonify(result), 200

@analysis_bp.route("/analysis", methods=["GET"])
def list_analyses():
    db_repo = get_analysis_repository()
    records = db_repo.list_analyses(limit=50)
    return jsonify({"success": True, "analyses": records}), 200

@analysis_bp.route("/analysis/<analysis_id>", methods=["GET"])
def get_analysis(analysis_id):
    db_repo = get_analysis_repository()
    record = db_repo.get_analysis(analysis_id)
    if not record:
        return jsonify({"success": False, "error": "Analysis record not found."}), 404
    return jsonify({"success": True, "data": record}), 200

@analysis_bp.route("/analysis/<analysis_id>", methods=["DELETE"])
def delete_analysis(analysis_id):
    db_repo = get_analysis_repository()
    record = db_repo.get_analysis(analysis_id)
    if not record:
        return jsonify({"success": False, "error": "Analysis record not found."}), 404

    resume_file_key = record.get("resume_file_key")
    if resume_file_key:
        storage_svc = get_storage_service()
        storage_svc.delete_file(resume_file_key)

    deleted = db_repo.delete_analysis(analysis_id)
    return jsonify({"success": deleted}), 200
