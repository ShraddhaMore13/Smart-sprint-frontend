import json
import numpy as np

class DeveloperRecommendationEngine:
    def __init__(self):
        self.skill_match_weights = {
            'exact': 1.0,
            'related': 0.7,
            'general': 0.4
        }
        self.historical_performance_weights = {
            'velocity': 0.6,
            'accuracy': 0.3,
            'sentiment': 0.1
        }
    
    def recommend_developers(self, ticket, developers, historical_data):
        recommendations = []
        
        for dev in developers:
            # Check if developer has enough availability
            if dev['current_workload'] + ticket['estimated_hours'] > dev['availability']:
                continue  # Skip developers who don't have enough availability
            
            # Get historical data for this developer, or use empty dict if none exists
            dev_history = historical_data.get(dev['id'], {})
            
            score = self._calculate_match_score(ticket, dev, dev_history)
            
            recommendations.append({
                'developer_id': dev['id'],
                'developer_name': dev['name'],
                'match_score': score,
                'skills_match': dev_history  # Use the actual historical data
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Return top 3
        return recommendations[:3]
    
    def _calculate_match_score(self, ticket, developer, historical_data):
        ticket_skills = self._extract_skills_from_ticket(ticket)
        dev_skills = developer['skills']
        
        skill_score = self._calculate_skill_match(ticket_skills, dev_skills)
        availability_score = self._calculate_availability(developer)
        historical_score = self._calculate_historical_performance(historical_data)
        
        # Add experience level factor (if available)
        experience_factor = developer.get('experience_level', 3) / 5  # Normalize to 0-1
        
        return (skill_score * 0.4) + (availability_score * 0.3) + (historical_score * 0.2) + (experience_factor * 0.1)
    
    def _extract_skills_from_ticket(self, ticket):
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
    
    def _calculate_skill_match(self, ticket_skills, dev_skills):
        if not ticket_skills:
            return 0.5
        
        total_score = 0
        matched_skills = 0
        
        for skill in ticket_skills:
            if skill in dev_skills:
                total_score += self.skill_match_weights['exact']
                matched_skills += 1
            else:
                for dev_skill in dev_skills:
                    if skill in dev_skill or dev_skill in skill:
                        total_score += self.skill_match_weights['related']
                        matched_skills += 1
                        break
        
        return min(1.0, total_score / len(ticket_skills))
    
    def _calculate_availability(self, developer):
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
    
    def _calculate_historical_performance(self, historical_data):
        if not historical_data:
            return 0.5
        
        velocity = historical_data.get('velocity', 1.0)
        accuracy = historical_data.get('accuracy', 1.0)
        sentiment = historical_data.get('sentiment', 1.0)
        
        return (velocity * self.historical_performance_weights['velocity'] +
                accuracy * self.historical_performance_weights['accuracy'] +
                sentiment * self.historical_performance_weights['sentiment'])