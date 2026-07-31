from flask import Blueprint, request, jsonify

from services.database import get_analysis_repository

dash_bp = Blueprint("dashboard_api", __name__, url_prefix="/api/dashboard")


@dash_bp.route("/stats", methods=["GET"])
def get_dashboard_stats():
    """Get aggregated dashboard statistics."""
    repo = get_analysis_repository()
    records = repo.list_analyses(limit=1000)

    if not records:
        return jsonify({
            "success": True,
            "stats": {
                "total_analyses": 0,
                "avg_general_score": 0,
                "avg_job_match_score": None,
                "total_interviews": 0,
                "avg_interview_score": 0,
                "top_skills": [],
                "weak_skills": [],
                "recent_analyses": [],
                "score_trend": []
            }
        })

    # Filter analysis types
    analyses = [r for r in records if not (isinstance(r.get("results_json", {}), dict) and r.get("results_json", {}).get("type") == "interview")]
    interviews = [r for r in records if isinstance(r.get("results_json", {}), dict) and r.get("results_json", {}).get("type") == "interview"]

    # Calculate averages
    general_scores = [r.get("general_score", 0) for r in analyses if r.get("general_score")]
    job_match_scores = [r.get("job_match_score", 0) for r in analyses if r.get("job_match_score") is not None]

    avg_general = int(sum(general_scores) / len(general_scores)) if general_scores else 0
    avg_job_match = int(sum(job_match_scores) / len(job_match_scores)) if job_match_scores else None

    # Interview stats
    interview_scores = [r.get("general_score", 0) for r in interviews if r.get("general_score")]
    avg_interview = int(sum(interview_scores) / len(interview_scores)) if interview_scores else 0

    # Aggregate skills from all analyses
    all_skills = {}
    for r in analyses:
        results = r.get("results_json", {})
        if isinstance(results, str):
            import json
            try:
                results = json.loads(results)
            except:
                results = {}
        detected = results.get("detected_skills", []) if isinstance(results, dict) else []
        for skill in detected:
            all_skills[skill] = all_skills.get(skill, 0) + 1

    sorted_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)
    top_skills = [s[0] for s in sorted_skills[:10]]
    weak_skills = [s[0] for s in sorted_skills[-5:] if len(sorted_skills) > 5]

    # Score trend (last 10 analyses)
    recent_analyses = analyses[:10]
    score_trend = [
        {
            "date": r.get("created_at", ""),
            "general_score": r.get("general_score", 0)
        }
        for r in recent_analyses
    ]

    return jsonify({
        "success": True,
        "stats": {
            "total_analyses": len(analyses),
            "avg_general_score": avg_general,
            "avg_job_match_score": avg_job_match,
            "total_interviews": len(interviews),
            "avg_interview_score": avg_interview,
            "top_skills": top_skills,
            "weak_skills": weak_skills,
            "recent_analyses": [
                {
                    "id": r.get("analysis_id"),
                    "filename": r.get("resume_filename", "Unknown"),
                    "score": r.get("general_score", 0),
                    "date": r.get("created_at", "")
                }
                for r in recent_analyses
            ],
            "score_trend": score_trend
        }
    })


@dash_bp.route("/trends", methods=["GET"])
def get_trends():
    """Get score trends over time."""
    repo = get_analysis_repository()
    records = repo.list_analyses(limit=100)

    # Filter non-interview analyses
    analyses = []
    for r in records:
        results = r.get("results_json", {})
        if isinstance(results, str):
            import json
            try:
                results = json.loads(results)
            except:
                results = {}
        if not (isinstance(results, dict) and results.get("type") == "interview"):
            analyses.append(r)

    trend_data = []
    for r in analyses:
        trend_data.append({
            "date": r.get("created_at", ""),
            "general_score": r.get("general_score", 0),
            "job_match_score": r.get("job_match_score")
        })

    return jsonify({
        "success": True,
        "trends": trend_data
    })

