from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime
import faiss
import json

class MemoryIndex:
    def __init__(self, dimension: int = 256):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.id_to_vector: Dict[str, np.ndarray] = {}
        self.id_to_metadata: Dict[str, Dict[str, Any]] = {}

    def add_memory(self, memory_id: str, vector: np.ndarray, metadata: Dict[str, Any]) -> None:
        """Add a memory vector to the index."""
        if vector.shape[0] != self.dimension:
            raise ValueError(f"Vector dimension {vector.shape[0]} does not match index dimension {self.dimension}")
        
        self.index.add(vector.reshape(1, -1))
        self.id_to_vector[memory_id] = vector
        self.id_to_metadata[memory_id] = metadata

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[tuple[str, float, Dict[str, Any]]]:
        """Search for similar memories."""
        distances, indices = self.index.search(query_vector.reshape(1, -1), k)
        
        results = []
        for i, distance in zip(indices[0], distances[0]):
            if i != -1:  # Valid index
                memory_id = list(self.id_to_vector.keys())[i]
                results.append((memory_id, float(distance), self.id_to_metadata[memory_id]))
        
        return results

    def save(self, path: str) -> None:
        """Save the index to disk."""
        faiss.write_index(self.index, f"{path}/vector_index.faiss")
        with open(f"{path}/metadata.json", 'w') as f:
            json.dump({
                'id_to_metadata': self.id_to_metadata,
                'dimension': self.dimension
            }, f)

    @classmethod
    def load(cls, path: str) -> 'MemoryIndex':
        """Load an index from disk."""
        with open(f"{path}/metadata.json", 'r') as f:
            metadata = json.load(f)
        
        index = cls(dimension=metadata['dimension'])
        index.index = faiss.read_index(f"{path}/vector_index.faiss")
        index.id_to_metadata = metadata['id_to_metadata']
        return index