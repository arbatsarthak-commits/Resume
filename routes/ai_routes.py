from flask import Blueprint, request, jsonify

from core.ai_service import get_ai_service

ai_bp = Blueprint("ai_api", __name__, url_prefix="/api/ai")

# ============================================================
# PROFESSIONAL SUMMARY
# ============================================================

@ai_bp.route("/summary", methods=["POST"])
def generate_summary():
    """Generate a professional summary based on user's skills and experience."""
    data = request.get_json() or {}
    skills = data.get("skills", [])
    experience_years = data.get("experience_years", "")
    current_role = data.get("current_role", "")
    top_achievements = data.get("achievements", [])

    ai = get_ai_service()
    summary = ai.generate_professional_summary(
        skills=skills,
        experience_years=experience_years,
        current_role=current_role,
        top_achievements=top_achievements
    )

    return jsonify({
        "success": True,
        "summary": summary,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# IMPROVE BULLET POINTS
# ============================================================

@ai_bp.route("/improve-bullets", methods=["POST"])
def improve_bullets():
    """Improve wording of bullet points."""
    data = request.get_json() or {}
    text = data.get("text", "")
    context = data.get("context", "")

    if not text:
        return jsonify({"success": False, "error": "No text provided."}), 400

    ai = get_ai_service()
    improved = ai.improve_bullet_points(text, context)

    return jsonify({
        "success": True,
        "original": text,
        "improved": improved,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# REWRITE EXPERIENCE
# ============================================================

@ai_bp.route("/rewrite-experience", methods=["POST"])
def rewrite_experience():
    """Rewrite work experience description."""
    data = request.get_json() or {}
    description = data.get("description", "")
    role = data.get("role", "")
    company = data.get("company", "")

    if not description:
        return jsonify({"success": False, "error": "No description provided."}), 400

    ai = get_ai_service()
    rewritten = ai.rewrite_experience(description, role, company)

    return jsonify({
        "success": True,
        "original": description,
        "improved": rewritten,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# IMPROVE PROJECT DESCRIPTION
# ============================================================

@ai_bp.route("/improve-project", methods=["POST"])
def improve_project():
    """Improve project description wording."""
    data = request.get_json() or {}
    description = data.get("description", "")
    tech_stack = data.get("tech_stack", "")

    if not description:
        return jsonify({"success": False, "error": "No description provided."}), 400

    ai = get_ai_service()
    improved = ai.improve_project_description(description, tech_stack)

    return jsonify({
        "success": True,
        "original": description,
        "improved": improved,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# GENERATE ACHIEVEMENT STATEMENT
# ============================================================

@ai_bp.route("/achievement", methods=["POST"])
def generate_achievement():
    """Generate an achievement statement using STAR method."""
    data = request.get_json() or {}
    role = data.get("role", "")
    context = data.get("context", "")
    action = data.get("action", "")

    if not action:
        return jsonify({"success": False, "error": "Action description is required."}), 400

    ai = get_ai_service()
    statement = ai.generate_achievement_statement(role, context, action)

    return jsonify({
        "success": True,
        "statement": statement,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# IMPROVE SKILLS REPRESENTATION
# ============================================================

@ai_bp.route("/skills", methods=["POST"])
def improve_skills():
    """Improve skills categorization and representation."""
    data = request.get_json() or {}
    skills = data.get("skills", [])
    categories = data.get("categories", {})

    ai = get_ai_service()
    improved = ai.improve_skills_representation(skills, categories)

    return jsonify({
        "success": True,
        "improved": improved,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# SUGGEST KEYWORDS
# ============================================================

@ai_bp.route("/keywords", methods=["POST"])
def suggest_keywords():
    """Suggest better keywords based on existing skills."""
    data = request.get_json() or {}
    skills = data.get("skills", [])
    job_title = data.get("job_title", "")

    ai = get_ai_service()
    suggestions = ai.suggest_keywords(skills, job_title)

    return jsonify({
        "success": True,
        "suggestions": suggestions,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# GENERATE RESUME HEADLINE
# ============================================================

@ai_bp.route("/headline", methods=["POST"])
def generate_headline():
    """Generate a professional resume headline."""
    data = request.get_json() or {}
    name = data.get("name", "")
    current_role = data.get("current_role", "")
    experience_years = data.get("experience_years", "")
    top_skills = data.get("top_skills", [])

    ai = get_ai_service()
    headline = ai.generate_resume_headline(name, current_role, experience_years, top_skills)

    return jsonify({
        "success": True,
        "headline": headline,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# GENERATE COVER LETTER
# ============================================================

@ai_bp.route("/cover-letter", methods=["POST"])
def generate_cover_letter():
    """Generate a professional cover letter."""
    data = request.get_json() or {}
    name = data.get("name", "")
    company = data.get("company", "")
    role = data.get("role", "")
    skills = data.get("skills", [])
    experience_summary = data.get("experience_summary", "")

    if not company or not role:
        return jsonify({"success": False, "error": "Company name and role are required."}), 400

    ai = get_ai_service()
    letter = ai.generate_cover_letter(name, company, role, skills, experience_summary)

    return jsonify({
        "success": True,
        "cover_letter": letter,
        "ai_assisted": ai.ai_available
    })

# ============================================================
# TAILOR RESUME FOR JOB DESCRIPTION
# ============================================================

@ai_bp.route("/tailor", methods=["POST"])
def tailor_resume():
    """Get suggestions for tailoring resume to a job description."""
    data = request.get_json() or {}
    resume_data = data.get("resume_data", {})
    jd_text = data.get("jd_text", "")
    matched_skills = data.get("matched_skills", [])
    missing_skills = data.get("missing_skills", [])

    if not jd_text:
        return jsonify({"success": False, "error": "Job description text is required."}), 400

    ai = get_ai_service()
    suggestions = ai.tailor_resume_for_jd(resume_data, jd_text, matched_skills, missing_skills)

    return jsonify({
        "success": True,
        "suggestions": suggestions,
        "ai_assisted": ai.ai_available
    })

