import numpy as np
from collections import defaultdict

class WorkloadBalancer:
    def __init__(self):
        self.developer_capacity = {}
        self.task_complexity_weights = {
            1: 1.0,
            2: 1.5,
            3: 2.0,
            4: 3.0,
            5: 4.0
        }
    
    def calculate_developer_capacity(self, developer, historical_data):
        """Calculate effective capacity of a developer considering historical performance"""
        base_capacity = developer['availability']
        
        # Get historical performance data
        perf_data = historical_data.get(developer['id'], {})
        velocity = perf_data.get('velocity', 1.0)
        accuracy = perf_data.get('accuracy', 1.0)
        
        # Adjust capacity based on performance
        effective_capacity = base_capacity * velocity * accuracy
        
        # Consider current workload
        current_load = developer['current_workload']
        available_capacity = effective_capacity - current_load
        
        return {
            'base_capacity': base_capacity,
            'effective_capacity': effective_capacity,
            'available_capacity': available_capacity,
            'utilization': current_load / effective_capacity if effective_capacity > 0 else 1.0
        }
    
    def calculate_task_weight(self, ticket):
        """Calculate the weight of a task considering complexity and priority"""
        complexity_weight = self.task_complexity_weights.get(ticket['complexity'], 2.0)
        
        priority_weights = {
            'low': 0.8,
            'medium': 1.0,
            'high': 1.3,
            'critical': 1.6
        }
        priority_weight = priority_weights.get(ticket['priority'], 1.0)
        
        # Base weight is estimated hours adjusted by complexity and priority
        base_weight = ticket['estimated_hours']
        adjusted_weight = base_weight * complexity_weight * priority_weight
        
        return adjusted_weight
    
    def optimize_workload(self, tickets, developers, historical_data):
        """Optimize workload distribution across developers"""
        # Filter unassigned tickets
        unassigned_tickets = [t for t in tickets if t.get('status') == 'backlog']
        
        if not unassigned_tickets:
            return []
        
        # Calculate developer capacities
        developer_capacities = {}
        for dev in developers:
            developer_capacities[dev['id']] = self.calculate_developer_capacity(dev, historical_data)
        
        # Sort tickets by priority and weight
        sorted_tickets = sorted(unassigned_tickets, 
                               key=lambda t: (t['priority'] != 'low', 
                                            t['priority'] != 'medium',
                                            t['priority'] != 'high',
                                            -self.calculate_task_weight(t)))
        
        assignments = []
        
        for ticket in sorted_tickets:
            # Find best developer for this ticket
            best_developer = None
            best_score = -1
            
            for dev in developers:
                capacity = developer_capacities[dev['id']]
                task_weight = self.calculate_task_weight(ticket)
                
                # Check if developer has capacity
                if capacity['available_capacity'] < task_weight:
                    continue
                
                # Calculate match score
                skill_match = self._calculate_skill_match(ticket, dev)
                availability_score = 1.0 - capacity['utilization']
                
                # Get historical performance
                perf_data = historical_data.get(dev['id'], {})
                velocity = perf_data.get('velocity', 1.0)
                accuracy = perf_data.get('accuracy', 1.0)
                
                # Calculate overall score
                score = (skill_match * 0.4) + (availability_score * 0.3) + (velocity * 0.2) + (accuracy * 0.1)
                
                if score > best_score:
                    best_score = score
                    best_developer = dev
            
            if best_developer:
                # Make assignment
                assignments.append({
                    'ticket_id': ticket['id'],
                    'developer_id': best_developer['id'],
                    'score': best_score
                })
                
                # Update developer capacity
                task_weight = self.calculate_task_weight(ticket)
                developer_capacities[best_developer['id']]['available_capacity'] -= task_weight
                developer_capacities[best_developer['id']]['utilization'] = (
                    developer_capacities[best_developer['id']]['effective_capacity'] - 
                    developer_capacities[best_developer['id']]['available_capacity']
                ) / developer_capacities[best_developer['id']]['effective_capacity']
        
        return assignments
    
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
    
    def balance_workload(self, developers, historical_data):
        """Balance workload among developers by suggesting task reassignments"""
        # Calculate current workload distribution
        workload_distribution = []
        total_capacity = 0
        total_workload = 0
        
        for dev in developers:
            capacity = self.calculate_developer_capacity(dev, historical_data)
            workload_distribution.append({
                'developer_id': dev['id'],
                'developer_name': dev['name'],
                'current_workload': dev['current_workload'],
                'effective_capacity': capacity['effective_capacity'],
                'utilization': capacity['utilization']
            })
            total_capacity += capacity['effective_capacity']
            total_workload += dev['current_workload']
        
        # Calculate average utilization
        avg_utilization = total_workload / total_capacity if total_capacity > 0 else 0
        
        # Identify overutilized and underutilized developers
        overutilized = [d for d in workload_distribution if d['utilization'] > avg_utilization + 0.1]
        underutilized = [d for d in workload_distribution if d['utilization'] < avg_utilization - 0.1]
        
        # Generate rebalancing suggestions
        suggestions = []
        
        for over_dev in overutilized:
            for under_dev in underutilized:
                # Calculate potential transfer amount
                over_capacity = over_dev['effective_capacity']
                under_capacity = under_dev['effective_capacity']
                
                # Suggest transferring tasks to balance workload
                transfer_amount = min(
                    over_dev['current_workload'] - (over_capacity * avg_utilization),
                    (under_capacity * avg_utilization) - under_dev['current_workload']
                )
                
                if transfer_amount > 1:  # Only suggest if significant
                    suggestions.append({
                        'from_developer': over_dev['developer_name'],
                        'to_developer': under_dev['developer_name'],
                        'transfer_hours': transfer_amount,
                        'reason': f"Balance workload from {over_dev['utilization']:.1%} to {under_dev['utilization']:.1%} utilization"
                    })
        
        return {
            'average_utilization': avg_utilization,
            'workload_distribution': workload_distribution,
            'suggestions': suggestions
        }