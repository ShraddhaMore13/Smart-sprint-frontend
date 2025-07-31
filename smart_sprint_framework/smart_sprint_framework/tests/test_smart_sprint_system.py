import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_sprint_system import SmartSprintSystem
from data_generator import generate_small_developers_csv, generate_small_sprint_documents_csv, generate_small_performance_data

class TestSmartSprintSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate test data
        generate_small_developers_csv()
        generate_small_sprint_documents_csv()
        generate_small_performance_data()
        
        # Initialize system
        cls.system = SmartSprintSystem()
    
    def test_system_initialization(self):
        """Test that the system initializes correctly"""
        self.assertIsNotNone(self.system.tickets)
        self.assertIsNotNone(self.system.developers)
        self.assertGreater(len(self.system.tickets), 0)
        self.assertGreater(len(self.system.developers), 0)
    
    def test_process_feature_story(self):
        """Test processing a feature story into a ticket"""
        feature_story = {
            "title": "Test Feature",
            "description": "This is a test feature",
            "priority": "medium",
            "estimated_hours": 8
        }
        
        initial_ticket_count = len(self.system.tickets)
        ticket = self.system.process_feature_story(feature_story)
        
        self.assertEqual(len(self.system.tickets), initial_ticket_count + 1)
        self.assertEqual(ticket['title'], feature_story['title'])
        self.assertEqual(ticket['priority'], feature_story['priority'])
        self.assertEqual(ticket['status'], 'backlog')
    
    def test_get_ticket_recommendations(self):
        """Test getting ticket recommendations"""
        # Get a ticket from backlog
        backlog_tickets = [t for t in self.system.tickets if t['status'] == 'backlog']
        if backlog_tickets:
            ticket = backlog_tickets[0]
            recommendations = self.system.get_ticket_recommendations(ticket['id'])
            
            # Should return a list (possibly empty)
            self.assertIsInstance(recommendations, list)
    
    def test_assign_developer_to_ticket(self):
        """Test assigning a developer to a ticket"""
        # Get a ticket from backlog
        backlog_tickets = [t for t in self.system.tickets if t['status'] == 'backlog']
        if backlog_tickets and self.system.developers:
            ticket = backlog_tickets[0]
            developer = self.system.developers[0]
            
            # Assign developer to ticket
            success = self.system.assign_developer_to_ticket(ticket['id'], developer['id'])
            
            if success:
                # Check that ticket is now assigned and in progress
                self.assertEqual(ticket['assigned_to'], developer['id'])
                self.assertEqual(ticket['status'], 'in_progress')
                self.assertGreater(developer['current_workload'], 0)
    
    def test_complete_ticket(self):
        """Test completing a ticket"""
        # Get a ticket that's in progress
        in_progress_tickets = [t for t in self.system.tickets if t['status'] == 'in_progress']
        if in_progress_tickets:
            ticket = in_progress_tickets[0]
            developer_id = ticket['assigned_to']
            
            # Complete the ticket
            success = self.system.complete_ticket(
                ticket['id'],
                completion_time=10,
                revisions=1,
                sentiment_score=0.8
            )
            
            if success:
                # Check that ticket is now completed
                self.assertEqual(ticket['status'], 'completed')
                
                # Check that developer's workload was reduced
                developer = next((d for d in self.system.developers if d['id'] == developer_id), None)
                if developer:
                    self.assertEqual(developer['current_workload'], 0)
    
    def test_get_system_status(self):
        """Test getting system status"""
        status = self.system.get_system_status()
        
        # Check that status contains expected keys
        expected_keys = [
            'total_tickets',
            'completed_tickets',
            'in_progress_tickets',
            'backlog_tickets',
            'total_workload',
            'total_availability',
            'utilization_rate'
        ]
        
        for key in expected_keys:
            self.assertIn(key, status)
    
    def test_get_developer_performance(self):
        """Test getting developer performance"""
        if self.system.developers:
            developer = self.system.developers[0]
            performance = self.system.get_developer_performance(developer['id'])
            
            # Performance may be None if no data exists
            if performance:
                self.assertIn('average_completion_time', performance)
                self.assertIn('accuracy', performance)
                self.assertIn('total_completed_tickets', performance)
                self.assertIn('average_sentiment', performance)

if __name__ == '__main__':
    unittest.main()