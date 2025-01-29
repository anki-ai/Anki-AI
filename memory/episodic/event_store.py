from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import json

class Event:
    def __init__(self, data: Dict[str, Any], timestamp: Optional[datetime] = None):
        self.id = str(uuid.uuid4())
        self.timestamp = timestamp or datetime.now()
        self.data = data
        self.tags: List[str] = []
        self.references: List[str] = []  # IDs of related events

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'tags': self.tags,
            'references': self.references
        }

class EventStore:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.events: Dict[str, Event] = {}
        self.index: Dict[str, List[str]] = {}  # tag -> event_ids

    def store_event(self, event: Event) -> str:
        """Store a new event and return its ID."""
        self.events[event.id] = event
        
        # Update indices
        for tag in event.tags:
            if tag not in self.index:
                self.index[tag] = []
            self.index[tag].append(event.id)
            
        self._persist_event(event)
        return event.id

    def get_event(self, event_id: str) -> Optional[Event]:
        """Retrieve an event by ID."""
        return self.events.get(event_id)

    def query_events(self, tags: List[str], start_time: Optional[datetime] = None,
                    end_time: Optional[datetime] = None) -> List[Event]:
        """Query events by tags and time range."""
        event_ids = set()
        for tag in tags:
            if tag in self.index:
                event_ids.update(self.index[tag])
        
        events = [self.events[eid] for eid in event_ids]
        
        # Apply time filters
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
            
        return sorted(events, key=lambda e: e.timestamp)

    def _persist_event(self, event: Event) -> None:
        """Save event to persistent storage."""
        with open(f"{self.storage_path}/{event.id}.json", 'w') as f:
            json.dump(event.to_dict(), f)