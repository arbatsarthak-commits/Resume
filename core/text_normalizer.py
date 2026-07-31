import re
import unicodedata

def normalize_text(text: str) -> str:
    """Normalizes whitespace and unicode characters while preserving linebreaks."""
    if not text:
        return ""

    # Normalize NFKD unicode (convert accents, symbols)
    text = unicodedata.normalize("NFKD", text)

    # Standardize bullet characters to simple dashes
    text = re.sub(r'[\u2022\u2023\u25e6\u2043\u2219\u25aa\u25ab]', '-', text)

    # Normalize multiple horizontal spaces into single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove excessive blank lines (> 2 newlines -> 2 newlines)
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)

    return text.strip()

def clean_tokens(text: str) -> str:
    """Converts text to lowercase with alphanumerics and basic symbols for keyword matching."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#\.\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
