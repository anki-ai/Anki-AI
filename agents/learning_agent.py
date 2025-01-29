from typing import Any, Dict, List
from ..base.agent import Agent
from ..base.memory import Memory
import numpy as np
from datetime import datetime

class LearningAgent(Agent):
    """An agent that learns from experiences and adapts its behavior."""
    
    def __init__(self, agent_id: str, memory: Memory, 
                 learning_rate: float = 0.1,
                 exploration_rate: float = 0.2):
        super().__init__(agent_id, memory)
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.knowledge_base: Dict[str, Any] = {}
        self.action_history: List[Dict[str, Any]] = []

    def perceive(self, observation: Dict[str, Any]) -> None:
        """Process and store new observations with context."""
        self.update_state(observation)
        
        # Enhance observation with context
        enhanced_observation = {
            'timestamp': datetime.now(),
            'type': 'observation',
            'data': observation,
            'context': self._extract_context(),
            'state': self.current_state.copy()
        }
        
        self.memory.store_experience(enhanced_observation)

    def decide(self) -> Any:
        """Make a decision using learned knowledge and exploration."""
        if np.random.random() < self.exploration_rate:
            # Explore: try a new random action
            return self._generate_exploratory_action()
        else:
            # Exploit: use learned knowledge
            similar_experiences = self.memory.retrieve_similar(
                {'state': self.current_state},
                limit=5
            )
            return self._select_best_action(similar_experiences)

    def act(self, action: Any) -> None:
        """Execute action and record it with metadata."""
        if action:
            action_record = {
                'timestamp': datetime.now(),
                'type': 'action',
                'data': action,
                'state': self.current_state.copy(),
                'context': self._extract_context()
            }
            
            self.action_history.append(action_record)
            self.memory.store_experience(action_record)
            # Execute action logic here
            pass

    def learn(self) -> None:
        """Learn from recent experiences and update knowledge base."""
        recent_experiences = self.memory.retrieve_similar(
            {'type': 'action'},
            limit=20
        )
        
        # Analyze outcomes
        for exp in recent_experiences:
            outcome = self._evaluate_outcome(exp)
            self._update_knowledge(exp, outcome)
        
        # Adjust exploration rate based on performance
        self._adjust_exploration_rate()
        
        # Consolidate memory periodically
        self.memory.consolidate_memory()

    def _extract_context(self) -> Dict[str, Any]:
        """Extract relevant context from current state."""
        return {
            'time_of_day': datetime.now().hour,
            'recent_actions': self.action_history[-5:] if self.action_history else [],
            'state_summary': self._summarize_state()
        }

    def _summarize_state(self) -> Dict[str, Any]:
        """Create a summary of current state."""
        # Implementation of state summarization
        return {}

    def _generate_exploratory_action(self) -> Any:
        """Generate a new action for exploration."""
        # Implementation of exploration strategy
        return None

    def _select_best_action(self, similar_experiences: List[Dict[str, Any]]) -> Any:
        """Select the best action based on similar past experiences."""
        if not similar_experiences:
            return self._generate_exploratory_action()
            
        # Find the action with the best outcome
        best_experience = max(similar_experiences, 
                            key=lambda x: self._evaluate_outcome(x))
        return best_experience.get('data')

    def _evaluate_outcome(self, experience: Dict[str, Any]) -> float:
        """Evaluate the outcome of an experience."""
        # Implementation of outcome evaluation
        return 0.0

    def _update_knowledge(self, experience: Dict[str, Any], outcome: float) -> None:
        """Update knowledge base with new experience."""
        key = self._generate_knowledge_key(experience)
        if key not in self.knowledge_base:
            self.knowledge_base[key] = {
                'count': 0,
                'average_outcome': 0.0
            }
        
        entry = self.knowledge_base[key]
        entry['count'] += 1
        entry['average_outcome'] = (entry['average_outcome'] * (entry['count'] - 1) + 
                                  outcome) / entry['count']

    def _adjust_exploration_rate(self) -> None:
        """Adjust exploration rate based on learning progress."""
        # Decay exploration rate over time
        self.exploration_rate *= 0.995  # Gradual reduction
        self.exploration_rate = max(0.05, self.exploration_rate)  # Minimum 5% exploration

    def _generate_knowledge_key(self, experience: Dict[str, Any]) -> str:
        """Generate a unique key for storing experience in knowledge base."""
        # Implementation of key generation
        return str(hash(str(experience.get('state', {}))))