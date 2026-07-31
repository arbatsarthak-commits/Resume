from core.ats_scorer import calculate_general_score, calculate_job_match_score

def test_ats_scoring_determinism():
    sections = {
        "contact": True, "education": True, "experience": True, 
        "projects": True, "skills": True, "summary": True, "certifications": True
    }
    contact_info = {"email": "test@example.com", "phone": "1234567890", "linkedin": "linkedin.com/in/test"}
    skills_data = {
        "detected_skills": ["Python", "AWS", "Docker", "Flask", "React"],
        "categorized_skills": {"Languages": ["Python"], "Cloud": ["AWS"]}
    }
    raw_text = "Sample resume text content with sufficient length to pass formatting hygiene checks." * 15

    score1 = calculate_general_score(sections, contact_info, skills_data, raw_text)
    score2 = calculate_general_score(sections, contact_info, skills_data, raw_text)

    # Must be 100% deterministic (exact same result)
    assert score1["total_score"] == score2["total_score"]
    assert score1["total_score"] >= 75
    assert score1["breakdown"]["contact"] == 10
    assert score1["breakdown"]["structure"] == 25

def test_job_match_scoring():
    gen_breakdown = {"experience": 15, "projects": 15, "structure": 25, "contact": 10, "formatting": 10}
    jd_match_data = {"skill_match_ratio": 0.8, "keyword_match_ratio": 0.7}

    job_score = calculate_job_match_score(gen_breakdown, jd_match_data)
    assert job_score["total_score"] > 50
    assert job_score["breakdown"]["skills"] == 20
    assert job_score["breakdown"]["keywords"] == 21
