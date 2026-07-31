from typing import Dict, Any, Optional

def calculate_general_score(
    sections: Dict[str, bool],
    contact_info: Dict[str, Any],
    skills_data: Dict[str, Any],
    raw_text: str
) -> Dict[str, Any]:
    """
    Calculates deterministic General Resume Quality Score (out of 100).
    Breakdown:
      Structure: 25
      Contact Information: 10
      Skills: 20
      Experience: 15
      Projects: 15
      Formatting: 10
      Certifications: 5
    """
    # 1. Structure Score (Max 25)
    structure_score = 0
    if sections.get("contact"): structure_score += 4
    if sections.get("education"): structure_score += 5
    if sections.get("experience"): structure_score += 5
    if sections.get("projects"): structure_score += 4
    if sections.get("skills"): structure_score += 4
    if sections.get("summary"): structure_score += 2
    if sections.get("certifications") or sections.get("achievements"): structure_score += 1

    # 2. Contact Information Score (Max 10)
    contact_score = 0
    if contact_info.get("email"): contact_score += 4
    if contact_info.get("phone"): contact_score += 4
    if contact_info.get("linkedin") or contact_info.get("github") or contact_info.get("portfolio"):
        contact_score += 2

    # 3. Skills Score (Max 20)
    num_skills = len(skills_data.get("detected_skills", []))
    num_categories = len(skills_data.get("categorized_skills", {}))
    skills_score = min(20, (num_skills * 2) + (num_categories * 2))

    # 4. Experience Score (Max 15)
    exp_score = 0
    if sections.get("experience"):
        exp_score = 10
        # bonus for action verbs / length
        if len(raw_text) > 800:
            exp_score += 5

    # 5. Projects Score (Max 15)
    proj_score = 0
    if sections.get("projects"):
        proj_score = 10
        if len(raw_text) > 1000:
            proj_score += 5

    # 6. Formatting Score (Max 10)
    formatting_score = 10
    if len(raw_text.strip()) < 150:
        formatting_score -= 5
    if len(raw_text.strip()) > 8000:  # excessively long resume
        formatting_score -= 3

    # 7. Certifications Score (Max 5)
    cert_score = 5 if (sections.get("certifications") or sections.get("achievements")) else 0

    total_general = structure_score + contact_score + skills_score + exp_score + proj_score + formatting_score + cert_score
    total_general = min(100, max(0, total_general))

    return {
        "total_score": total_general,
        "breakdown": {
            "structure": structure_score,
            "contact": contact_score,
            "skills": skills_score,
            "experience": exp_score,
            "projects": proj_score,
            "formatting": formatting_score,
            "certifications": cert_score
        }
    }


def calculate_job_match_score(
    general_breakdown: Dict[str, int],
    jd_match_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculates deterministic Job-Specific Match Score (out of 100).
    Breakdown:
      Keyword Match: 30
      Skills Match: 25
      Experience Relevance: 15
      Projects Relevance: 10
      Resume Structure: 10
      Contact Information: 5
      Formatting: 5
    """
    keyword_ratio = jd_match_data.get("keyword_match_ratio", 0.0)
    skill_ratio = jd_match_data.get("skill_match_ratio", 0.0)

    keyword_score = round(keyword_ratio * 30)
    skills_match_score = round(skill_ratio * 25)

    # Experience relevance based on general experience score ratio
    exp_rel_score = round((general_breakdown.get("experience", 0) / 15) * 15)

    # Projects relevance based on general projects score ratio
    proj_rel_score = round((general_breakdown.get("projects", 0) / 15) * 10)

    # Structure (max 10)
    struct_score = round((general_breakdown.get("structure", 0) / 25) * 10)

    # Contact (max 5)
    contact_score = round((general_breakdown.get("contact", 0) / 10) * 5)

    # Formatting (max 5)
    fmt_score = round((general_breakdown.get("formatting", 0) / 10) * 5)

    total_job_match = keyword_score + skills_match_score + exp_rel_score + proj_rel_score + struct_score + contact_score + fmt_score
    total_job_match = min(100, max(0, total_job_match))

    return {
        "total_score": total_job_match,
        "breakdown": {
            "keywords": keyword_score,
            "skills": skills_match_score,
            "experience": exp_rel_score,
            "projects": proj_rel_score,
            "structure": struct_score,
            "contact": contact_score,
            "formatting": fmt_score
        }
    }
