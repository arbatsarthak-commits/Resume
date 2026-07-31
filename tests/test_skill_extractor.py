from core.skill_extractor import extract_skills

def test_extract_skills_aliases_and_boundaries():
    text = "Proficient in Python, C, C++, ReactJS, React.js, Amazon Web Services, Docker, and PostgreSQL."
    res = extract_skills(text)
    skills = res["detected_skills"]

    assert "Python" in skills
    assert "C" in skills
    assert "C++" in skills
    assert "React" in skills
    assert "AWS" in skills
    assert "Docker" in skills
    assert "PostgreSQL" in skills

def test_extract_skills_no_false_c_match():
    # Word 'cat' or 'location' contains letter 'c', but should NOT trigger 'C' language match
    text = "I am located in California working on documentation and computer design."
    res = extract_skills(text)
    skills = res["detected_skills"]

    assert "C" not in skills
