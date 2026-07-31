from flask import Blueprint, request, jsonify

from core.interview_engine import get_interview_engine, InterviewQuestion, AnswerEvaluation

interview_bp = Blueprint("interview_api", __name__, url_prefix="/api/interview")


@interview_bp.route("/questions", methods=["POST"])
def generate_questions():
    """Generate interview questions based on type and context."""
    data = request.get_json() or {}
    interview_type = data.get("type", "mixed")
    resume_data = data.get("resume_data")
    jd_text = data.get("jd_text")
    count = min(int(data.get("count", 5)), 20)
    difficulty = data.get("difficulty", "medium")

    engine = get_interview_engine()
    questions = engine.generate_questions(
        interview_type=interview_type,
        resume_data=resume_data,
        jd_text=jd_text,
        count=count,
        difficulty=difficulty
    )

    return jsonify({
        "success": True,
        "questions": [
            {
                "id": q.id,
                "type": q.type,
                "category": q.category,
                "question": q.question,
                "difficulty": q.difficulty,
                "options": q.options if q.type == "mcq" else [],
                "expected_keywords": q.expected_keywords
            }
            for q in questions
        ],
        "count": len(questions),
        "ai_assisted": engine.ai_available
    })


@interview_bp.route("/evaluate", methods=["POST"])
def evaluate_answer():
    """Evaluate a user's answer to an interview question."""
    data = request.get_json() or {}
    question_data = data.get("question", {})
    answer = data.get("answer", "")

    if not answer or not answer.strip():
        return jsonify({"success": False, "error": "No answer provided."}), 400

    question = InterviewQuestion(
        id=question_data.get("id", "unknown"),
        type=question_data.get("type", "technical"),
        category=question_data.get("category", "General"),
        question=question_data.get("question", ""),
        difficulty=question_data.get("difficulty", "medium"),
        expected_keywords=question_data.get("expected_keywords", []),
        sample_answer=question_data.get("sample_answer", ""),
        options=question_data.get("options", []),
        correct_option=question_data.get("correct_option", -1)
    )

    engine = get_interview_engine()
    evaluation = engine.evaluate_answer(question, answer)

    return jsonify({
        "success": True,
        "evaluation": {
            "communication": evaluation.communication,
            "completeness": evaluation.completeness,
            "technical_accuracy": evaluation.technical_accuracy,
            "confidence": evaluation.confidence,
            "grammar": evaluation.grammar,
            "star_method": evaluation.star_method,
            "overall_score": evaluation.overall_score,
            "good_points": evaluation.good_points,
            "weak_points": evaluation.weak_points,
            "missing_concepts": evaluation.missing_concepts,
            "better_answer": evaluation.better_answer
        },
        "ai_assisted": engine.ai_available
    })


@interview_bp.route("/readiness", methods=["POST"])
def calculate_readiness():
    """Calculate interview readiness score."""
    data = request.get_json() or {}
    resume_score = data.get("resume_score")
    ats_score = data.get("ats_score")
    interview_performance_data = data.get("interview_performance", [])
    job_match_score = data.get("job_match_score")
    skill_coverage = data.get("skill_coverage")

    # Convert performance data to AnswerEvaluation objects
    interview_performance = []
    for perf in interview_performance_data:
        interview_performance.append(AnswerEvaluation(
            communication=perf.get("communication", 0),
            completeness=perf.get("completeness", 0),
            technical_accuracy=perf.get("technical_accuracy", 0),
            confidence=perf.get("confidence", 0),
            grammar=perf.get("grammar", 0),
            star_method=perf.get("star_method", 0),
            overall_score=perf.get("overall_score", 0)
        ))

    engine = get_interview_engine()
    readiness = engine.calculate_readiness_score(
        resume_score=resume_score,
        ats_score=ats_score,
        interview_performance=interview_performance if interview_performance else None,
        job_match_score=job_match_score,
        skill_coverage=skill_coverage
    )

    return jsonify({
        "success": True,
        "readiness": readiness,
        "ai_assisted": engine.ai_available
    })


@interview_bp.route("/session/save", methods=["POST"])
def save_session():
    """Save an interview session to history."""
    from services.database import get_analysis_repository
    import uuid
    from datetime import datetime

    data = request.get_json() or {}
    session_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    session_data = {
        "session_id": session_id,
        "analysis_id": session_id,
        "created_at": created_at,
        "interview_type": data.get("type", "mixed"),
        "resume_filename": "interview_session",
        "general_score": data.get("average_score", 0),
        "results_json": {
            "type": "interview",
            "session_id": session_id,
            "questions": data.get("questions", []),
            "answers": data.get("answers", []),
            "evaluations": data.get("evaluations", []),
            "readiness": data.get("readiness", {}),
            "summary": data.get("summary", {})
        }
    }

    repo = get_analysis_repository()
    repo.save_analysis(session_data)

    return jsonify({
        "success": True,
        "session_id": session_id
    })


@interview_bp.route("/history", methods=["GET"])
def get_history():
    """Get interview session history."""
    from services.database import get_analysis_repository

    repo = get_analysis_repository()
    records = repo.list_analyses(limit=50)

    # Filter to interview sessions only
    interview_sessions = []
    for record in records:
        results = record.get("results_json", {})
        if isinstance(results, dict) and results.get("type") == "interview":
            interview_sessions.append({
                "session_id": record.get("session_id") or record.get("analysis_id"),
                "created_at": record.get("created_at"),
                "interview_type": record.get("interview_type", "mixed"),
                "average_score": record.get("general_score", 0),
                "question_count": len(results.get("questions", [])),
                "readiness": results.get("readiness", {})
            })

    return jsonify({
        "success": True,
        "sessions": interview_sessions
    })


@interview_bp.route("/session/<session_id>", methods=["GET"])
def get_session(session_id):
    """Get a specific interview session details."""
    from services.database import get_analysis_repository

    repo = get_analysis_repository()
    record = repo.get_analysis(session_id)
    if not record:
        return jsonify({"success": False, "error": "Session not found."}), 404

    return jsonify({
        "success": True,
        "session": record
    })


@interview_bp.route("/session/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    """Delete an interview session."""
    from services.database import get_analysis_repository

    repo = get_analysis_repository()
    deleted = repo.delete_analysis(session_id)
    return jsonify({"success": deleted})

