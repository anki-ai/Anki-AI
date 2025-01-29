from typing import Any, Dict, List
from ..base.agent import Agent
from ..base.memory import Memory

class ReactiveAgent(Agent):
    """A simple reactive agent that responds to immediate stimuli."""
    
    def __init__(self, agent_id: str, memory: Memory, reaction_rules: Dict[str, Any]):
        super().__init__(agent_id, memory)
        self.reaction_rules = reaction_rules

    def perceive(self, observation: Dict[str, Any]) -> None:
        """Process new observations and store them in current state."""
        self.update_state(observation)
        # Store observation in short-term memory
        self.memory.store_experience({
            'timestamp': observation.get('timestamp'),
            'type': 'observation',
            'data': observation
        })

    def decide(self) -> Any:
        """Make a decision based on current state and reaction rules."""
        for condition, action in self.reaction_rules.items():
            if self._evaluate_condition(condition):
                return action
        return None

    def act(self, action: Any) -> None:
        """Execute the chosen action and store it in memory."""
        if action:
            self.memory.store_experience({
                'timestamp': datetime.now(),
                'type': 'action',
                'data': action
            })
            # Execute action logic here
            pass

    def learn(self) -> None:
        """Basic learning mechanism - update reaction rules based on success."""
        # Simple learning implementation
        recent_experiences = self.memory.retrieve_similar(
            {'type': 'action'},
            limit=10
        )
        self._update_rules(recent_experiences)

    def _evaluate_condition(self, condition: str) -> bool:
        """Evaluate if a condition is met based on current state."""
        # Implementation of condition evaluation
        return True

    def _update_rules(self, experiences: List[Dict[str, Any]]) -> None:
        """Update reaction rules based on recent experiences."""
        pass