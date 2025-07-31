import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from developer_recommendation import DeveloperRecommendationEngine

class TestDeveloperRecommendationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DeveloperRecommendationEngine()
        
        # Sample data
        self.ticket = {
            'id': 1,
            'title': 'Test Ticket',
            'description': 'This is a test ticket requiring API development',
            'priority': 'medium',
            'complexity': 3,
            'estimated_hours': 16
        }
        
        self.developers = [
            {
                'id': 1,
                'name': 'John Doe',
                'skills': ['python', 'api', 'database'],
                'availability': 40,
                'current_workload': 0,
                'experience_level': 4
            },
            {
                'id': 2,
                'name': 'Jane Smith',
                'skills': ['javascript', 'react', 'frontend'],
                'availability': 40,
                'current_workload': 0,
                'experience_level': 3
            }
        ]
        
        self.historical_data = {
            1: {
                'velocity': 1.2,
                'accuracy': 0.9,
                'sentiment': 0.8,
                'tickets_completed': 10
            },
            2: {
                'velocity': 0.9,
                'accuracy': 0.8,
                'sentiment': 0.7,
                'tickets_completed': 8
            }
        }
    
    def test_recommend_developers(self):
        """Test developer recommendation"""
        recommendations = self.engine.recommend_developers(
            self.ticket, self.developers, self.historical_data
        )
        
        # Should return a list
        self.assertIsInstance(recommendations, list)
        
        # Should have at most 3 recommendations
        self.assertLessEqual(len(recommendations), 3)
        
        # Each recommendation should have required fields
        for rec in recommendations:
            self.assertIn('developer_id', rec)
            self.assertIn('developer_name', rec)
            self.assertIn('match_score', rec)
    
    def test_skill_match_calculation(self):
        """Test skill match calculation"""
        # Test exact match
        ticket_skills = ['api', 'database']
        dev_skills = ['python', 'api', 'frontend']
        match_score = self.engine._calculate_skill_match(
            {'title': 'Test', 'description': 'Test'}, 
            {'skills': dev_skills}, 
            ticket_skills
        )
        
        self.assertGreater(match_score, 0.5)
        self.assertLessEqual(match_score, 1.0)
    
    def test_availability_calculation(self):
        """Test availability calculation"""
        # Test high availability
        developer = {
            'availability': 40,
            'current_workload': 10
        }
        availability_score = self.engine._calculate_availability(developer)
        self.assertGreater(availability_score, 0.5)
        
        # Test low availability
        developer = {
            'availability': 40,
            'current_workload': 35
        }
        availability_score = self.engine._calculate_availability(developer)
        self.assertLess(availability_score, 0.5)

if __name__ == '__main__':
    unittest.main()