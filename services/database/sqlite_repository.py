import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from config import Config
from services.database.base import AnalysisRepository

class SQLiteAnalysisRepository(AnalysisRepository):
    """SQLite implementation of AnalysisRepository for local mode."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    resume_filename TEXT,
                    resume_file_key TEXT,
                    general_score INTEGER,
                    job_match_score INTEGER,
                    results_json TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_analysis(self, analysis_data: Dict[str, Any]) -> str:
        analysis_id = analysis_data.get("analysis_id")
        if not analysis_id:
            raise ValueError("Analysis data must contain 'analysis_id'")
            
        created_at = analysis_data.get("created_at") or datetime.utcnow().isoformat()
        resume_filename = analysis_data.get("resume_filename", "resume.pdf")
        resume_file_key = analysis_data.get("resume_file_key", "")
        general_score = analysis_data.get("general_score", 0)
        job_match_score = analysis_data.get("job_match_score")

        results_json = json.dumps(analysis_data)

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO analyses (
                    id, created_at, resume_filename, resume_file_key, 
                    general_score, job_match_score, results_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    general_score=excluded.general_score,
                    job_match_score=excluded.job_match_score,
                    results_json=excluded.results_json
            """, (
                analysis_id, created_at, resume_filename, resume_file_key,
                general_score, job_match_score, results_json
            ))
            conn.commit()

        return analysis_id

    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT results_json FROM analyses WHERE id = ?", (analysis_id,))
            row = cursor.fetchone()
            if row:
                return json.loads(row["results_json"])
            return None

    def list_analyses(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, created_at, resume_filename, resume_file_key, general_score, job_match_score, results_json 
                FROM analyses 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                data = json.loads(row["results_json"])
                results.append(data)
            return results

    def delete_analysis(self, analysis_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
            conn.commit()
            return cursor.rowcount > 0
