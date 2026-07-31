import re
from typing import Dict, Optional, Any

EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_REGEX = r'(?:\+\d{1,3}[\s-]?)?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}'
LINKEDIN_REGEX = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?'
GITHUB_REGEX = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+/?'
URL_REGEX = r'(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'

def detect_contact_info(text: str) -> Dict[str, Any]:
    """Detects email, phone, LinkedIn, GitHub, portfolio URLs, and candidate name."""
    info = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "portfolio": None,
        "name": None,
        "has_contact_info": False
    }

    if not text:
        return info

    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Candidate Name heuristic (typically top 1-3 lines, non-email/phone/url)
    for line in lines[:3]:
        if not re.search(EMAIL_REGEX, line) and not re.search(PHONE_REGEX, line) and not re.search(r'http|www|resume|curriculum', line, re.IGNORECASE):
            if len(line.split()) <= 4 and re.match(r'^[A-Za-z\s\.\'-]+$', line):
                info["name"] = line
                break

    # Email
    emails = re.findall(EMAIL_REGEX, text)
    if emails:
        info["email"] = emails[0]

    # Phone
    phones = re.findall(PHONE_REGEX, text)
    if phones:
        # Filter phone candidates that look like dates or standard numbers
        valid_phones = [p.strip() for p in phones if len(re.sub(r'\D', '', p)) >= 10]
        if valid_phones:
            info["phone"] = valid_phones[0]

    # LinkedIn
    linkedin_match = re.search(LINKEDIN_REGEX, text, re.IGNORECASE)
    if linkedin_match:
        info["linkedin"] = linkedin_match.group(0)

    # GitHub
    github_match = re.search(GITHUB_REGEX, text, re.IGNORECASE)
    if github_match:
        info["github"] = github_match.group(0)

    # General Portfolio URL (if not linkedin/github)
    urls = re.findall(URL_REGEX, text)
    for url in urls:
        if "linkedin.com" not in url.lower() and "github.com" not in url.lower():
            info["portfolio"] = url
            break

    info["has_contact_info"] = bool(info["email"] or info["phone"])
    return info
