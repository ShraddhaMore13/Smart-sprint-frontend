import numpy as np
import random
from collections import defaultdict

class RLTaskAssignment:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.state_space = set()
        self.action_space = set()
    
    def get_state(self, ticket, developer):
        """Create a state representation"""
        # Simplified state representation
        skill_match = self._calculate_skill_match(ticket, developer)
        availability = developer['availability'] - developer['current_workload']
        workload_ratio = developer['current_workload'] / developer['availability'] if developer['availability'] > 0 else 1
        
        # Discretize continuous values
        skill_level = 'high' if skill_match > 0.7 else 'medium' if skill_match > 0.4 else 'low'
        availability_level = 'high' if availability > 20 else 'medium' if availability > 10 else 'low'
        workload_level = 'high' if workload_ratio > 0.8 else 'medium' if workload_ratio > 0.5 else 'low'
        
        state = (skill_level, availability_level, workload_level, ticket['priority'])
        return state
    
    def get_action(self, state, developers, training=True):
        """Choose an action (developer assignment) using epsilon-greedy policy"""
        if training and random.random() < self.exploration_rate:
            # Explore: choose random developer
            return random.choice(developers)
        else:
            # Exploit: choose best developer based on Q-values
            q_values = [self.q_table[state][dev['id']] for dev in developers]
            max_q = max(q_values) if q_values else 0
            best_developers = [dev for dev, q in zip(developers, q_values) if q == max_q]
            return random.choice(best_developers)
    
    def update_q_value(self, state, action, reward, next_state):
        """Update Q-value using Q-learning algorithm"""
        current_q = self.q_table[state][action['id']]
        
        # Get maximum Q-value for next state
        next_max_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        
        # Q-learning update rule
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state][action['id']] = new_q
    
    def calculate_reward(self, ticket, developer, completion_time, revisions, sentiment_score):
        """Calculate reward based on performance metrics"""
        # Base reward
        reward = 0
        
        # Reward for on-time completion
        if completion_time <= ticket['estimated_hours'] * 1.2:
            reward += 10
        else:
            reward -= 5
        
        # Penalty for revisions
        reward -= revisions * 2
        
        # Reward for high sentiment
        reward += sentiment_score * 5
        
        # Reward for skill match
        skill_match = self._calculate_skill_match(ticket, developer)
        reward += skill_match * 3
        
        return reward
    
    def _calculate_skill_match(self, ticket, developer):
        """Calculate skill match between ticket and developer"""
        ticket_skills = self._extract_skills_from_ticket(ticket)
        dev_skills = developer['skills']
        
        if not ticket_skills:
            return 0.5
        
        exact_matches = sum(1 for skill in ticket_skills if skill in dev_skills)
        related_matches = 0
        for skill in ticket_skills:
            if skill not in dev_skills:
                for dev_skill in dev_skills:
                    if skill in dev_skill or dev_skill in skill:
                        related_matches += 1
                        break
        
        total_matches = exact_matches + related_matches * 0.7
        return min(1.0, total_matches / len(ticket_skills))
    
    def _extract_skills_from_ticket(self, ticket):
        """Extract required skills from ticket title and description"""
        text = f"{ticket['title']} {ticket['description']}".lower()
        skills = []
        
        if 'auth' in text or 'login' in text:
            skills.append('auth')
        if 'database' in text or 'sql' in text:
            skills.append('database')
        if 'api' in text or 'endpoint' in text:
            skills.append('api')
        if 'frontend' in text or 'ui' in text or 'react' in text:
            skills.append('frontend')
        if 'backend' in text or 'server' in text:
            skills.append('backend')
        
        return skills
    
    def train(self, tickets, developers, performance_data, episodes=100):
        """Train the RL model"""
        print("Training RL model for task assignment...")
        
        for episode in range(episodes):
            # Shuffle tickets for each episode
            shuffled_tickets = random.sample(tickets, len(tickets))
            
            for ticket in shuffled_tickets:
                if ticket.get('status') != 'completed':
                    continue
                
                developer = next((d for d in developers if d['id'] == ticket['assigned_to']), None)
                if not developer:
                    continue
                
                # Get current state
                state = self.get_state(ticket, developer)
                
                # Choose action (in training, we use the actual assignment)
                action = developer
                
                # Get next state (simplified - using same state for now)
                next_state = state
                
                # Calculate reward
                perf_data = performance_data.get(developer['id'], {})
                completion_time = ticket.get('completion_time', ticket['estimated_hours'])
                revisions = perf_data.get('revisions', 0)
                sentiment_score = perf_data.get('sentiment', 0.7)
                
                reward = self.calculate_reward(ticket, developer, completion_time, revisions, sentiment_score)
                
                # Update Q-value
                self.update_q_value(state, action, reward, next_state)
            
            # Decay exploration rate
            self.exploration_rate = max(0.01, self.exploration_rate * 0.995)
            
            if episode % 10 == 0:
                print(f"Episode {episode}/{episodes}, Exploration rate: {self.exploration_rate:.3f}")
        
        print("RL model training completed!")
    
    def recommend_developer(self, ticket, developers, training=False):
        """Recommend a developer for a ticket using trained RL model"""
        # Filter developers with enough availability
        available_developers = [d for d in developers 
                               if d['current_workload'] + ticket['estimated_hours'] <= d['availability']]
        
        if not available_developers:
            return None
        
        # Get state for the ticket
        # We'll use a dummy developer to get the state representation
        dummy_state = self.get_state(ticket, available_developers[0])
        
        # Choose action (developer)
        developer = self.get_action(dummy_state, available_developers, training)
        
        return developer
    
    def _calculate_availability_score(self, developer):
        """Calculate availability score for a developer"""
        current_workload = developer['current_workload']
        availability = developer['availability']
        
        if current_workload >= availability:
            return 0.1
        elif current_workload >= availability * 0.8:
            return 0.3
        elif current_workload >= availability * 0.5:
            return 0.7
        else:
            return 1.0