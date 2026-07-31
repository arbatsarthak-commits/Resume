from flask import Blueprint, request, jsonify
from core.jd_matcher import match_job_description
from core.skill_extractor import extract_skills
from core.keyword_extractor import extract_keywords
from core.text_normalizer import normalize_text

job_bp = Blueprint("job_api", __name__, url_prefix="/api")

@job_bp.route("/jobs/match", methods=["POST"])
def match_job():
    data = request.get_json() or {}
    jd_text = data.get("job_description")
    resume_text = data.get("resume_text")
    provided_skills = data.get("skills", [])

    if not jd_text or not jd_text.strip():
        return jsonify({"success": False, "error": "Job description text is required."}), 400

    if resume_text:
        normalized = normalize_text(resume_text)
        extracted = extract_skills(normalized)
        resume_skills = extracted["detected_skills"]
        resume_keywords = extract_keywords(normalized)
    else:
        resume_skills = provided_skills
        resume_keywords = data.get("keywords", [])

    match_result = match_job_description(
        resume_skills=resume_skills,
        resume_keywords=resume_keywords,
        jd_text=jd_text
    )

    return jsonify({"success": True, "match": match_result}), 200
