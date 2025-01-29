from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

class Sequence:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.events: List[str] = []  # List of event IDs
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.metadata: Dict[str, Any] = {}

class SequenceStore:
    def __init__(self):
        self.sequences: Dict[str, Sequence] = {}
        self.event_to_sequence: Dict[str, List[str]] = {}  # event_id -> sequence_ids

    def create_sequence(self, name: str) -> Sequence:
        """Create a new sequence."""
        sequence = Sequence(name)
        self.sequences[sequence.id] = sequence
        return sequence

    def add_event_to_sequence(self, sequence_id: str, event_id: str) -> None:
        """Add an event to a sequence."""
        if sequence_id in self.sequences:
            sequence = self.sequences[sequence_id]
            sequence.events.append(event_id)
            
            if event_id not in self.event_to_sequence:
                self.event_to_sequence[event_id] = []
            self.event_to_sequence[event_id].append(sequence_id)

    def get_sequences_for_event(self, event_id: str) -> List[Sequence]:
        """Get all sequences containing an event."""
        sequence_ids = self.event_to_sequence.get(event_id, [])
        return [self.sequences[sid] for sid in sequence_ids]