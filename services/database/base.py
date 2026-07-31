from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class AnalysisRepository(ABC):
    """Abstract interface for storing and retrieving analysis results."""

    @abstractmethod
    def save_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Saves an analysis result dict and returns the generated/provided analysis_id."""
        pass

    @abstractmethod
    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single analysis result by ID."""
        pass

    @abstractmethod
    def list_analyses(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Lists previous analysis records ordered by creation date descending."""
        pass

    @abstractmethod
    def delete_analysis(self, analysis_id: str) -> bool:
        """Deletes an analysis record by ID."""
        pass
