from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

class Fact:
    def __init__(self, subject: str, predicate: str, object: Any,
                 confidence: float = 1.0):
        self.id = str(uuid.uuid4())
        self.subject = subject
        self.predicate = predicate
        self.object = object
        self.confidence = confidence
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        self.supporting_evidence: List[str] = []  # Event IDs that support this fact

class FactStore:
    def __init__(self):
        self.facts: Dict[str, Fact] = {}
        self.subject_index: Dict[str, List[str]] = {}
        self.predicate_index: Dict[str, List[str]] = {}

    def add_fact(self, fact: Fact) -> str:
        """Add a new fact to the store."""
        self.facts[fact.id] = fact
        
        # Update indices
        if fact.subject not in self.subject_index:
            self.subject_index[fact.subject] = []
        self.subject_index[fact.subject].append(fact.id)
        
        if fact.predicate not in self.predicate_index:
            self.predicate_index[fact.predicate] = []
        self.predicate_index[fact.predicate].append(fact.id)
        
        return fact.id

    def query_facts(self, subject: Optional[str] = None,
                   predicate: Optional[str] = None) -> List[Fact]:
        """Query facts by subject and/or predicate."""
        fact_ids = set()
        
        if subject:
            fact_ids.update(self.subject_index.get(subject, []))
        if predicate:
            fact_ids.update(self.predicate_index.get(predicate, []))
            
        if subject and predicate:
            # Intersection if both filters are applied
            subject_facts = set(self.subject_index.get(subject, []))
            predicate_facts = set(self.predicate_index.get(predicate, []))
            fact_ids = subject_facts.intersection(predicate_facts)
            
        return [self.facts[fid] for fid in fact_ids]