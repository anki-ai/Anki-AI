from typing import Dict, List, Optional, Any
import numpy as np
from datetime import datetime

class Concept:
    def __init__(self, name: str, features: Dict[str, Any]):
        self.name = name
        self.features = features
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        self.related_concepts: Dict[str, float] = {}  # concept_name -> similarity
        self.examples: List[str] = []  # Event IDs that exemplify this concept

class ConceptStore:
    def __init__(self):
        self.concepts: Dict[str, Concept] = {}
        self.feature_vectors: Dict[str, np.ndarray] = {}

    def add_concept(self, concept: Concept) -> None:
        """Add a new concept to the store."""
        self.concepts[concept.name] = concept
        self._update_feature_vector(concept)
        self._update_relationships(concept)

    def find_similar_concepts(self, concept_name: str,
                            threshold: float = 0.5) -> List[tuple[str, float]]:
        """Find concepts similar to the given one."""
        if concept_name not in self.concepts:
            return []
            
        target_vector = self.feature_vectors[concept_name]
        similarities = []
        
        for name, vector in self.feature_vectors.items():
            if name != concept_name:
                similarity = self._compute_similarity(target_vector, vector)
                if similarity >= threshold:
                    similarities.append((name, similarity))
                    
        return sorted(similarities, key=lambda x: x[1], reverse=True)

    def _update_feature_vector(self, concept: Concept) -> None:
        """Create or update the feature vector for a concept."""
        # Convert features to vector representation
        vector = self._features_to_vector(concept.features)
        self.feature_vectors[concept.name] = vector

    def _update_relationships(self, concept: Concept) -> None:
        """Update relationships with other concepts."""
        vector = self.feature_vectors[concept.name]
        
        for other_name, other_vector in self.feature_vectors.items():
            if other_name != concept.name:
                similarity = self._compute_similarity(vector, other_vector)
                concept.related_concepts[other_name] = similarity
                self.concepts[other_name].related_concepts[concept.name] = similarity

    @staticmethod
    def _compute_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

    @staticmethod
    def _features_to_vector(features: Dict[str, Any]) -> np.ndarray:
        """Convert feature dictionary to vector representation."""
        # Implementation dependent on feature types
        return np.array([])