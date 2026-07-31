import io
from app import create_app

def test_page_routes():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    pages = ["/", "/builder", "/analyzer", "/matcher", "/dashboard", "/templates", "/about"]
    for route in pages:
        response = client.get(route)
        assert response.status_code == 200

def test_job_match_api():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    payload = {
        "resume_text": "Experienced Python backend developer working with Flask, Docker, and AWS.",
        "job_description": "We are looking for a Python developer with Docker experience."
    }

    response = client.post("/api/jobs/match", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "Python" in data["match"]["matched_skills"]
