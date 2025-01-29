from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .memory import Memory

class Agent(ABC):
    """Base agent class that defines the interface for all agents."""
    
    def __init__(self, agent_id: str, memory: Memory):
        self.agent_id = agent_id
        self.memory = memory
        self.current_state: Dict[str, Any] = {}

    @abstractmethod
    def perceive(self, observation: Dict[str, Any]) -> None:
        """Process new observations from the environment."""
        pass

    @abstractmethod
    def decide(self) -> Any:
        """Make a decision based on current state and memory."""
        pass

    @abstractmethod
    def act(self, action: Any) -> None:
        """Execute the chosen action."""
        pass

    @abstractmethod
    def learn(self) -> None:
        """Learn from recent experiences."""
        pass

    def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update the agent's current state."""
        self.current_state.update(new_state)