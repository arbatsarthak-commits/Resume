import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from core.pdf_parser import parse_pdf
from core.docx_parser import parse_docx
from core.text_normalizer import normalize_text
from core.section_detector import detect_sections
from core.contact_detector import detect_contact_info
from core.skill_extractor import extract_skills
from core.keyword_extractor import extract_keywords
from core.jd_matcher import match_job_description
from core.ats_scorer import calculate_general_score, calculate_job_match_score
from core.recommendation_engine import generate_recommendations

def process_resume_analysis(
    file_bytes: bytes,
    filename: str,
    jd_text: Optional[str] = None,
    resume_file_key: str = ""
) -> Dict[str, Any]:
    """
    Complete ATS processing pipeline for a resume document.
    """
    analysis_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in {"pdf", "docx"}:
        raise ValueError("Unsupported file format. Please upload a valid PDF or DOCX document.")

    # 1. Text Extraction
    if ext == "pdf":
        raw_text, parse_meta = parse_pdf(file_bytes)
    else:  # docx
        raw_text, parse_meta = parse_docx(file_bytes)

    # 2. Text Normalization
    normalized = normalize_text(raw_text)

    # 3. Section Detection
    sec_data = detect_sections(normalized)
    sections = sec_data["sections"]

    # 4. Contact Detection
    contact_info = detect_contact_info(normalized)

    # 5. Skill Extraction
    skills_data = extract_skills(normalized)

    # 6. Keyword Extraction
    resume_keywords = extract_keywords(normalized, top_n=30)

    # 7. General Score Calculation
    gen_score_data = calculate_general_score(
        sections=sections,
        contact_info=contact_info,
        skills_data=skills_data,
        raw_text=normalized
    )

    # 8. Job Description Match (Optional)
    jd_match_data = None
    job_match_score_data = None

    if jd_text and jd_text.strip():
        jd_match_data = match_job_description(
            resume_skills=skills_data["detected_skills"],
            resume_keywords=resume_keywords,
            jd_text=jd_text.strip()
        )
        job_match_score_data = calculate_job_match_score(
            general_breakdown=gen_score_data["breakdown"],
            jd_match_data=jd_match_data
        )

    # 9. Recommendation Engine
    recommendations = generate_recommendations(
        sections=sections,
        contact_info=contact_info,
        skills_data=skills_data,
        jd_match_data=jd_match_data
    )

    # Prepare response data structure matching spec
    result = {
        "success": True,
        "analysis_id": analysis_id,
        "created_at": created_at,
        "resume_filename": filename,
        "resume_file_key": resume_file_key,
        "general_score": gen_score_data["total_score"],
        "job_match_score": job_match_score_data["total_score"] if job_match_score_data else None,
        "score_breakdown": gen_score_data["breakdown"],
        "job_score_breakdown": job_match_score_data["breakdown"] if job_match_score_data else None,
        "detected_skills": skills_data["detected_skills"],
        "categorized_skills": skills_data["categorized_skills"],
        "matched_skills": jd_match_data["matched_skills"] if jd_match_data else [],
        "missing_skills": jd_match_data["missing_skills"] if jd_match_data else [],
        "matched_keywords": jd_match_data["matched_keywords"] if jd_match_data else [],
        "missing_keywords": jd_match_data["missing_keywords"] if jd_match_data else [],
        "sections": sections,
        "contact_info": contact_info,
        "recommendations": recommendations,
        "parse_metadata": parse_meta
    }

    return result
