import pytest
from core.pdf_parser import parse_pdf
from core.resume_builder_pdf import generate_resume_pdf

def test_parse_pdf_valid():
    # Generate a real PDF in memory
    sample_data = {
        "personal": {"full_name": "Alice Developer", "email": "alice@example.com"},
        "summary": "Experienced Python and AWS Cloud Developer.",
        "education": [{"institution": "MIT", "degree": "BS", "field": "Computer Science"}],
        "experience": [{"company": "Tech", "role": "Dev", "description": "Built REST APIs."}],
        "skills": {"Languages": ["Python", "C++"]}
    }
    pdf_bytes = generate_resume_pdf(sample_data)
    text, meta = parse_pdf(pdf_bytes)

    assert "ALICE DEVELOPER" in text.upper()
    assert "Python" in text
    assert meta["page_count"] >= 1
    assert meta["character_count"] > 50

def test_parse_pdf_empty():
    with pytest.raises(ValueError, match="empty"):
        parse_pdf(b"")

def test_parse_pdf_invalid_corrupt():
    with pytest.raises(ValueError):
        parse_pdf(b"Invalid PDF content string")
