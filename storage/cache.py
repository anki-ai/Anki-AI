from typing import Dict, Any, Optional, List
from collections import OrderedDict
from datetime import datetime, timedelta
import threading
import time

class CacheEntry:
    """Represents a single cache entry with metadata."""
    
    def __init__(self, data: Any, ttl: Optional[int] = None):
        self.data = data
        self.created_at = datetime.now()
        self.last_accessed = self.created_at
        self.access_count = 0
        self.expires_at = self.created_at + timedelta(seconds=ttl) if ttl else None

    def access(self) -> None:
        """Update access metadata."""
        self.last_accessed = datetime.now()
        self.access_count += 1

    def is_expired(self) -> bool:
        """Check if the entry has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

class MemoryCache:
    """LRU cache implementation with TTL support."""
    
    def __init__(self, capacity: int = 1000, cleanup_interval: int = 300):
        self.capacity = capacity
        self.cleanup_interval = cleanup_interval
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.lock = threading.Lock()
        
        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()

    def get(self, key: str) -> Optional[Any]:
        """Retrieve an item from the cache."""
        with self.lock:
            if key not in self.cache:
                return None
                
            entry = self.cache[key]
            if entry.is_expired():
                del self.cache[key]
                return None
                
            # Update access metadata and move to end (most recently used)
            entry.access()
            self.cache.move_to_end(key)
            return entry.data

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Add an item to the cache."""
        with self.lock:
            # Remove if already exists
            if key in self.cache:
                del self.cache[key]
                
            # Remove oldest if at capacity
            while len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
                
            # Add new entry
            self.cache[key] = CacheEntry(value, ttl)

    def delete(self, key: str) -> bool:
        """Remove an item from the cache."""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all items from the cache."""
        with self.lock:
            self.cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_items = len(self.cache)
            expired_items = sum(1 for entry in self.cache.values() if entry.is_expired())
            access_counts = [entry.access_count for entry in self.cache.values()]
            
            return {
                'total_items': total_items,
                'expired_items': expired_items,
                'capacity': self.capacity,
                'usage_percent': (total_items / self.capacity) * 100,
                'avg_access_count': sum(access_counts) / total_items if total_items > 0 else 0,
                'max_access_count': max(access_counts) if access_counts else 0
            }

    def get_keys(self) -> List[str]:
        """Get all valid (non-expired) keys in the cache."""
        with self.lock:
            return [
                key for key, entry in self.cache.items()
                if not entry.is_expired()
            ]

    def _cleanup_loop(self) -> None:
        """Background thread for removing expired entries."""
        while True:
            time.sleep(self.cleanup_interval)
            self._cleanup_expired()

    def _cleanup_expired(self) -> None:
        """Remove all expired entries from the cache."""
        with self.lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self.cache[key]

    def update_ttl(self, key: str, new_ttl: Optional[int]) -> bool:
        """Update the TTL for an existing cache entry."""
        with self.lock:
            if key not in self.cache:
                return False
                
            entry = self.cache[key]
            if new_ttl is None:
                entry.expires_at = None
            else:
                entry.expires_at = datetime.now() + timedelta(seconds=new_ttl)
            return True

    def touch(self, key: str) -> bool:
        """Update access time for an entry without retrieving it."""
        with self.lock:
            if key not in self.cache:
                return False
                
            entry = self.cache[key]
            if entry.is_expired():
                del self.cache[key]
                return False
                
            entry.access()
            self.cache.move_to_end(key)
            return True