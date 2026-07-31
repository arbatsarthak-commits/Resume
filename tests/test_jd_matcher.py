from core.jd_matcher import match_job_description

def test_match_job_description():
    resume_skills = ["Python", "AWS", "Docker", "Flask"]
    resume_keywords = ["developer", "backend", "rest", "api"]

    jd_text = """
    We are seeking a Senior Backend Engineer proficient in Python, AWS, Docker, PostgreSQL, and Kubernetes.
    Responsibilities include building REST APIs and managing containerized applications.
    """

    res = match_job_description(resume_skills, resume_keywords, jd_text)

    assert "Python" in res["matched_skills"]
    assert "AWS" in res["matched_skills"]
    assert "Docker" in res["matched_skills"]

    assert "PostgreSQL" in res["missing_skills"]
    assert "Kubernetes" in res["missing_skills"]

    assert res["skill_match_ratio"] < 1.0
