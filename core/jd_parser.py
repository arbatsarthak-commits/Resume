from typing import Dict, Any
from core.skill_extractor import extract_skills
from core.keyword_extractor import extract_keywords
from core.text_normalizer import normalize_text

def parse_job_description(jd_text: str) -> Dict[str, Any]:
    """
    Parses Job Description text to extract required technical skills and domain keywords.
    """
    if not jd_text or not jd_text.strip():
        return {
            "required_skills": [],
            "keywords": [],
            "raw_text": ""
        }

    normalized = normalize_text(jd_text)
    skill_res = extract_skills(normalized)
    keywords = extract_keywords(normalized, top_n=25)

    return {
        "required_skills": skill_res["detected_skills"],
        "keywords": keywords,
        "raw_text": normalized
    }
