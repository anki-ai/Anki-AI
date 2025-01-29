from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

class Memory(ABC):
    """Base memory interface that defines how agents store and retrieve experiences."""
    
    def __init__(self, capacity: Optional[int] = None):
        self.capacity = capacity
        self.creation_time = datetime.now()

    @abstractmethod
    def store_experience(self, experience: Dict[str, Any]) -> str:
        """Store a new experience and return its identifier."""
        pass

    @abstractmethod
    def retrieve_experience(self, experience_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific experience by its identifier."""
        pass

    @abstractmethod
    def retrieve_similar(self, query: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve experiences similar to the query."""
        pass

    @abstractmethod
    def update_experience(self, experience_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing experience."""
        pass

    @abstractmethod
    def consolidate_memory(self) -> None:
        """Consolidate and optimize stored memories."""
        pass