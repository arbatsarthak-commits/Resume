import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from config import Config
from services.database.base import AnalysisRepository

class DynamoDBAnalysisRepository(AnalysisRepository):
    """DynamoDB implementation of AnalysisRepository for AWS mode."""

    def __init__(self, table_name: str = None, region: str = None):
        self.table_name = table_name or Config.AWS_DYNAMODB_TABLE
        self.region = region or Config.AWS_REGION
        self._dynamodb_resource = None

    @property
    def table(self):
        if self._dynamodb_resource is None:
            import boto3
            self._dynamodb_resource = boto3.resource("dynamodb", region_name=self.region)
        return self._dynamodb_resource.Table(self.table_name)

    def save_analysis(self, analysis_data: Dict[str, Any]) -> str:
        analysis_id = analysis_data.get("analysis_id")
        if not analysis_id:
            raise ValueError("Analysis data must contain 'analysis_id'")

        created_at = analysis_data.get("created_at") or datetime.utcnow().isoformat()
        
        # DynamoDB requires clean float to Decimal conversion or json stringification for complex dicts
        item = {
            "analysis_id": analysis_id,
            "created_at": created_at,
            "resume_filename": analysis_data.get("resume_filename", "resume.pdf"),
            "resume_file_key": analysis_data.get("resume_file_key", ""),
            "general_score": int(analysis_data.get("general_score", 0)),
            "results_json": json.dumps(analysis_data)
        }
        if analysis_data.get("job_match_score") is not None:
            item["job_match_score"] = int(analysis_data.get("job_match_score"))

        self.table.put_item(Item=item)
        return analysis_id

    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.get_item(Key={"analysis_id": analysis_id})
            item = response.get("Item")
            if item and "results_json" in item:
                return json.loads(item["results_json"])
            return None
        except Exception:
            return None

    def list_analyses(self, limit: int = 50) -> List[Dict[str, Any]]:
        try:
            # DynamoDB scan or query
            response = self.table.scan(Limit=limit)
            items = response.get("Items", [])
            # Sort by created_at descending
            items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            results = []
            for item in items:
                if "results_json" in item:
                    results.append(json.loads(item["results_json"]))
            return results
        except Exception:
            return []

    def delete_analysis(self, analysis_id: str) -> bool:
        try:
            self.table.delete_item(Key={"analysis_id": analysis_id})
            return True
        except Exception:
            return False
