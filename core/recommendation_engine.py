from typing import Dict, List, Any, Optional

def generate_recommendations(
    sections: Dict[str, bool],
    contact_info: Dict[str, Any],
    skills_data: Dict[str, Any],
    jd_match_data: Optional[Dict[str, Any]] = None
) -> List[Dict[str, str]]:
    """
    Generates prioritized, non-fabricated optimization recommendations.
    Categories: HIGH, MEDIUM, LOW.
    """
    recs = []

    # 1. Contact Information Recommendations
    if not contact_info.get("email"):
        recs.append({
            "priority": "HIGH",
            "category": "Contact Information",
            "message": "Email address was not detected. Ensure your email is clearly visible at the top of your resume."
        })
    if not contact_info.get("phone"):
        recs.append({
            "priority": "HIGH",
            "category": "Contact Information",
            "message": "Phone number was not detected. Including a contact phone number is recommended for ATS parsers."
        })
    if not contact_info.get("linkedin"):
        recs.append({
            "priority": "MEDIUM",
            "category": "Contact Information",
            "message": "LinkedIn profile link was not detected. Adding a clean LinkedIn URL improves professional visibility."
        })

    # 2. Section Presence Recommendations
    if not sections.get("summary"):
        recs.append({
            "priority": "MEDIUM",
            "category": "Structure",
            "message": "Professional Summary section was not detected. A 2-3 line summary helps convey your core expertise quickly."
        })
    if not sections.get("experience"):
        recs.append({
            "priority": "HIGH",
            "category": "Structure",
            "message": "Work Experience section heading was not detected or clearly formatted. Ensure you use standard headers like 'Work Experience' or 'Professional Experience'."
        })
    if not sections.get("projects"):
        recs.append({
            "priority": "MEDIUM",
            "category": "Structure",
            "message": "Projects section was not detected. Including technical projects demonstrates practical application of your skills."
        })
    if not sections.get("skills"):
        recs.append({
            "priority": "HIGH",
            "category": "Structure",
            "message": "Technical Skills section heading was not detected. Grouping skills under a dedicated 'Technical Skills' header improves ATS keyword parsing."
        })

    # 3. Skills Recommendations
    detected_skills = skills_data.get("detected_skills", [])
    if len(detected_skills) < 5:
        recs.append({
            "priority": "HIGH",
            "category": "Skills",
            "message": "Fewer than 5 technical skills were detected. Ensure all relevant programming languages, frameworks, tools, and databases are listed."
        })

    # 4. Job Description Match Specific Recommendations
    if jd_match_data:
        missing_skills = jd_match_data.get("missing_skills", [])
        matched_skills = jd_match_data.get("matched_skills", [])
        jd_skills_count = jd_match_data.get("jd_skills_count", 0)

        if jd_skills_count > 0:
            recs.append({
                "priority": "MEDIUM",
                "category": "Job Match",
                "message": f"Your resume contains {len(matched_skills)} of the {jd_skills_count} key technical skills detected in the job description."
            })

        if missing_skills:
            top_missing = missing_skills[:5]
            missing_str = ", ".join(top_missing)
            recs.append({
                "priority": "HIGH",
                "category": "Skill Gap",
                "message": f"The following skills appear in the job description but were not detected in your resume: {missing_str}. If you genuinely possess experience in any of these, consider representing them clearly."
            })

    # Default general encouraging recommendation if few issues
    if len(recs) < 2:
        recs.append({
            "priority": "LOW",
            "category": "Optimization",
            "message": "Your resume structure and contact information are well-formatted. Ensure project and work descriptions use active bullet points emphasizing your impact."
        })

    return recs
