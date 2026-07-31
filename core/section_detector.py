import re
from typing import Dict, Any

SECTION_PATTERNS = {
    "summary": [
        r"professional summary", r"summary", r"profile", r"executive summary", 
        r"career objective", r"about me", r"objective"
    ],
    "education": [
        r"education", r"academic background", r"academic qualification", 
        r"academic qualifications", r"qualifications", r"academic history"
    ],
    "experience": [
        r"experience", r"work experience", r"professional experience", 
        r"employment history", r"work history", r"employment", r"career history"
    ],
    "projects": [
        r"projects", r"academic projects", r"personal projects", 
        r"project experience", r"key projects", r"technical projects"
    ],
    "skills": [
        r"skills", r"technical skills", r"core skills", r"key skills", 
        r"technologies", r"technical competencies", r"competencies", r"skills & tools"
    ],
    "certifications": [
        r"certifications", r"licenses", r"certifications & licenses", 
        r"certificates", r"training & certifications", r"courses"
    ],
    "achievements": [
        r"achievements", r"honors", r"awards", r"honors & awards", 
        r"key achievements", r"accomplishments"
    ],
    "leadership": [
        r"leadership", r"extracurricular", r"extra-curricular", 
        r"extracurricular activities", r"activities"
    ],
    "positions": [
        r"positions of responsibility", r"responsibility", r"positions", 
        r"volunteer", r"volunteering", r"volunteer experience"
    ]
}

def detect_sections(text: str) -> Dict[str, Any]:
    """
    Scans normalized resume text line by line to detect presence of key sections.
    Returns dict containing presence boolean flags and mapped line blocks.
    """
    lines = text.split('\n')
    detected_flags = {
        "summary": False,
        "education": False,
        "experience": False,
        "projects": False,
        "skills": False,
        "certifications": False,
        "achievements": False,
        "leadership": False,
        "positions": False,
        "contact": False
    }

    # Section text blocks accumulator
    section_texts = {sec: [] for sec in detected_flags.keys()}
    current_section = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        clean_line = re.sub(r'[^a-zA-Z0-9\s&]', '', stripped).strip().lower()

        # Header heuristic: line is short (<= 35 chars) or formatted like a title
        is_header_candidate = len(stripped) <= 40 and len(stripped.split()) <= 5

        found_section = None

        if is_header_candidate:
            for sec_key, patterns in SECTION_PATTERNS.items():
                for pat in patterns:
                    if clean_line == pat or clean_line.startswith(pat + ":") or clean_line.endswith(pat):
                        found_section = sec_key
                        break
                if found_section:
                    break

        if found_section:
            current_section = found_section
            detected_flags[found_section] = True
        elif current_section:
            section_texts[current_section].append(stripped)

    # Check if contact information was found near top or in text
    has_contact = len(text.strip()) > 0 and ("@" in text or re.search(r'\d{10}', text))
    detected_flags["contact"] = has_contact

    section_content_map = {k: "\n".join(v) for k, v in section_texts.items()}

    return {
        "sections": detected_flags,
        "section_content": section_content_map
    }
