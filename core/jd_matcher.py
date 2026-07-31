from typing import Dict, List, Any
from core.jd_parser import parse_job_description

def match_job_description(resume_skills: List[str], resume_keywords: List[str], jd_text: str) -> Dict[str, Any]:
    """
    Compares resume skills and keywords against job description requirements.
    """
    parsed_jd = parse_job_description(jd_text)
    jd_skills = parsed_jd["required_skills"]
    jd_keywords = parsed_jd["keywords"]

    resume_skills_set = set(s.lower() for s in resume_skills)
    resume_keywords_set = set(k.lower() for k in resume_keywords)

    matched_skills = []
    missing_skills = []

    for skill in jd_skills:
        if skill.lower() in resume_skills_set:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    matched_keywords = []
    missing_keywords = []

    for kw in jd_keywords:
        if kw.lower() in resume_keywords_set:
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    # Calculate skill match ratio
    skill_match_ratio = (len(matched_skills) / len(jd_skills)) if jd_skills else 1.0
    keyword_match_ratio = (len(matched_keywords) / len(jd_keywords)) if jd_keywords else 1.0

    return {
        "jd_skills_count": len(jd_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "jd_keywords_count": len(jd_keywords),
        "matched_keywords": sorted(matched_keywords),
        "missing_keywords": sorted(missing_keywords),
        "skill_match_ratio": round(skill_match_ratio, 2),
        "keyword_match_ratio": round(keyword_match_ratio, 2)
    }
