from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import heapq

class WorkingMemoryItem:
    def __init__(self, data: Any, priority: float = 0.0,
                 duration: Optional[timedelta] = None):
        self.data = data
        self.priority = priority
        self.created_at = datetime.now()
        self.expires_at = (self.created_at + duration) if duration else None
        self.access_count = 0
        self.last_accessed = self.created_at

class WorkingMemory:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.items: Dict[str, WorkingMemoryItem] = {}
        self.priority_queue: List[tuple[float, str]] = []  # [(priority, item_id)]

    def add_item(self, item_id: str, data: Any, priority: float = 0.0,
                duration: Optional[timedelta] = None) -> None:
        """Add an item to working memory."""
        if len(self.items) >= self.capacity:
            self._evict_items()
            
        item = WorkingMemoryItem(data, priority, duration)
        self.items[item_id] = item
        heapq.heappush(self.priority_queue, (-priority, item_id))

    def get_item(self, item_id: str) -> Optional[Any]:
        """Retrieve an item from working memory."""
        item = self.items.get(item_id)
        if item:
            if item.expires_at and datetime.now() > item.expires_at:
                self._remove_item(item_id)
                return None
                
            item.access_count += 1
            item.last_accessed = datetime.now()
            return item.data
        return None

    def update_priority(self, item_id: str, new_priority: float) -> None:
        """Update the priority of an item."""
        if item_id in self.items:
            item = self.items[item_id]
            item.priority = new_priority
            self._rebuild_priority_queue()

    def _evict_items(self) -> None:
        """Evict items based on priority and expiration."""
        current_time = datetime.now()
        
        # Remove expired items
        expired = [item_id for item_id, item in self.items.items()
                  if item.expires_at and current_time > item.expires_at]
        for item_id in expired:
            self._remove_item(item_id)
            
        # If still over capacity, remove lowest priority items
        while len(self.items) >= self.capacity:
            _, item_id = heapq.heappop(self.priority_queue)
            self._remove_item(item_id)

    def _remove_item(self, item_id: str) -> None:
        """Remove an item from working memory."""
        if item_id in self.items:
            del self.items[item_id]
            self._rebuild_priority_queue()

    def _rebuild_priority_queue(self) -> None:
        """Rebuild the priority queue."""
        self.priority_queue = [(-item.priority, item_id)
                             for item_id, item in self.items.items()]
        heapq.heapify(self.priority_queue)