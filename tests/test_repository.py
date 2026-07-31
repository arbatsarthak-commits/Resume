import os
import uuid
import tempfile
from services.database.sqlite_repository import SQLiteAnalysisRepository

def test_sqlite_repository_crud():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        repo = SQLiteAnalysisRepository(db_path=db_path)
        analysis_id = str(uuid.uuid4())
        
        sample_data = {
            "analysis_id": analysis_id,
            "resume_filename": "test_resume.pdf",
            "general_score": 85,
            "job_match_score": 75,
            "detected_skills": ["Python", "Flask"]
        }

        # 1. Save
        repo.save_analysis(sample_data)

        # 2. Get
        retrieved = repo.get_analysis(analysis_id)
        assert retrieved is not None
        assert retrieved["analysis_id"] == analysis_id
        assert retrieved["general_score"] == 85

        # 3. List
        history = repo.list_analyses()
        assert len(history) == 1
        assert history[0]["analysis_id"] == analysis_id

        # 4. Delete
        deleted = repo.delete_analysis(analysis_id)
        assert deleted is True
        assert repo.get_analysis(analysis_id) is None

    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
