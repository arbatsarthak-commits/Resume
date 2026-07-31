from core.section_detector import detect_sections

def test_detect_sections_complete():
    text = """
    John Doe
    Email: john@example.com | Phone: 1234567890

    Professional Summary
    Senior Software Engineer with experience building cloud web apps.

    Education
    Stanford University, B.S. Computer Science

    Work Experience
    Software Developer at Google. Developed microservices in Python.

    Projects
    ResumeIQ - Cloud Resume Builder built with Flask and AWS Lambda.

    Technical Skills
    Python, Flask, AWS, Docker, React, PostgreSQL

    Certifications
    AWS Certified Solutions Architect
    """
    res = detect_sections(text)
    secs = res["sections"]

    assert secs["summary"] is True
    assert secs["education"] is True
    assert secs["experience"] is True
    assert secs["projects"] is True
    assert secs["skills"] is True
    assert secs["certifications"] is True
    assert secs["contact"] is True
