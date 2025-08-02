import sqlite3
import os
import json
import random
import ast  # For parsing string representations of lists
from nlp_pipeline import NLPPipeline
from ticket_generator import TicketGenerator 
from developer_recommendation import DeveloperRecommendationEngine
from monte_carlo import MonteCarloEstimator
from performance_tracker import PerformanceTracker
from training_module import TrainingModule
from jira_integration import JiraIntegration
from rl_assignment import RLTaskAssignment
from gpt_simulation import GPTSimulation
from workload_balancer import WorkloadBalancer
from progress_monitor import ProgressMonitor
from dashboard_data import DashboardDataGenerator
import pandas as pd
import shutil
import datetime
import csv
from error_handler import (
    ValidationError, NotFoundError, ConflictError,
    safe_execute, retry_operation
)

class SmartSprintSystem:
    def __init__(self):
        self.tickets = []
        self.developers = []
        self.nlp = NLPPipeline()
        self.ticket_gen = TicketGenerator(self.nlp)
        self.recommendation_engine = DeveloperRecommendationEngine()
        self.performance_tracker = PerformanceTracker()
        self.monte_carlo = MonteCarloEstimator()
        self.training_module = TrainingModule()
        self.jira_integration = None
        self.jira_config = {}
        self.rl_assignment = RLTaskAssignment()
        self.gpt_simulation = GPTSimulation()
        self.workload_balancer = WorkloadBalancer()
        self.progress_monitor = ProgressMonitor()
        
        # Generate data files if they don't exist
        self._generate_data_files_if_missing()
        
        # Try to load Jira configuration
        try:
            with open('jira_config.json', 'r') as f:
                self.jira_config = json.load(f)
                self.jira_integration = JiraIntegration(
                    self.jira_config['url'],
                    self.jira_config['username'],
                    self.jira_config['api_token']
                )
                print("Jira integration initialized")
        except Exception as e:
            print(f"Jira integration not available: {e}")
        
        # Load data from small CSV files
        self._load_data_from_csv()
        
        # Try to load trained models if they exist
        self.training_module.load_models()
        
        # Train RL model if we have enough data
        completed_tickets = [t for t in self.tickets if t.get('status') == 'completed']
        if len(completed_tickets) >= 5:
            historical_data = self.performance_tracker.get_historical_performance_data()
            self.rl_assignment.train(self.tickets, self.developers, historical_data)
    
    def _generate_data_files_if_missing(self):
        """Generate data files if they don't exist"""
        import os
        
        # Check if data files exist
        files_exist = all([
            os.path.exists('developers_small.csv'),
            os.path.exists('sprint_documents_small.csv'),
            os.path.exists('performance_data_small.csv')
        ])
        
        if not files_exist:
            print("Data files missing. Generating sample data...")
            
            print("Data files missing. Please run the setup script first:")
            print("python setup_and_run.py")
            print("Or run the data generation script:")
            print("python generate_small_dataset.py")
            return False
        return True
    
    def _load_data_from_csv(self):
        # Load developers from small dataset
        try:
            developers_df = pd.read_csv('developers_small.csv')
            self.developers = []
            for index, row in developers_df.iterrows():
                dev = row.to_dict()
                
                # Handle skills - try to parse as list or string representation of list
                if isinstance(dev['skills'], str):
                    try:
                        # Try to parse as string representation of list
                        dev['skills'] = ast.literal_eval(dev['skills'])
                    except (ValueError, SyntaxError):
                        # If that fails, try splitting by comma
                        dev['skills'] = [skill.strip() for skill in dev['skills'].split(',')]
                
                # Ensure current_workload is a number
                if pd.isna(dev['current_workload']) or dev['current_workload'] == 'nan':
                    dev['current_workload'] = 0
                else:
                    try:
                        dev['current_workload'] = float(dev['current_workload'])
                    except (ValueError, TypeError):
                        dev['current_workload'] = 0
                
                # Ensure availability is a number
                if pd.isna(dev['availability']) or dev['availability'] == 'nan':
                    dev['availability'] = 40  # Default availability
                else:
                    try:
                        dev['availability'] = float(dev['availability'])
                    except (ValueError, TypeError):
                        dev['availability'] = 40  # Default availability
                
                # Ensure experience_level is a number
                if pd.isna(dev['experience_level']) or dev['experience_level'] == 'nan':
                    dev['experience_level'] = 3  # Default level
                else:
                    try:
                        dev['experience_level'] = int(dev['experience_level'])
                    except (ValueError, TypeError):
                        dev['experience_level'] = 3  # Default level
                
                # Validate required fields
                if not dev.get('name') or not dev.get('skills'):
                    print(f"Warning: Invalid developer data at index {index}, skipping")
                    continue
                    
                self.developers.append(dev)
            
            print(f"Loaded {len(self.developers)} developers from developers_small.csv")
        except Exception as e:
            print(f"Warning: Could not load developers_small.csv: {e}")
            self._generate_sample_developers()
    
        # Load tickets from small dataset
        try:
            tickets_df = pd.read_csv('sprint_documents_small.csv')
            self.tickets = []
            for index, row in tickets_df.iterrows():
                ticket = row.to_dict()
                
                # Convert tasks from string to list
                if isinstance(ticket['tasks'], str):
                    ticket['tasks'] = [task.strip() for task in ticket['tasks'].split(',')]
                
                # Handle assigned_to field properly
                if pd.isna(ticket['assigned_to']) or ticket['assigned_to'] == 'nan':
                    ticket['assigned_to'] = None
                else:
                    try:
                        ticket['assigned_to'] = int(ticket['assigned_to'])
                    except (ValueError, TypeError):
                        ticket['assigned_to'] = None
                
                # Ensure status is properly set
                if pd.isna(ticket['status']) or ticket['status'] == 'nan':
                    ticket['status'] = 'backlog'
                else:
                    ticket['status'] = str(ticket['status'])
                
                # Add entities field if missing
                if 'entities' not in ticket:
                    ticket['entities'] = {
                        'priorities': ['medium'],
                        'dependencies': [],
                        'deadlines': [],
                        'tasks': []
                    }
                
                self.tickets.append(ticket)
            
            print(f"Loaded {len(self.tickets)} tickets from sprint_documents_small.csv")
        except Exception as e:
            print(f"Warning: Could not load sprint_documents_small.csv: {e}")
            self._generate_sample_tickets()
        
        # Load performance data from small dataset
        try:
            performance_df = pd.read_csv('performance_data_small.csv')
            self.performance_tracker.metrics = []
            for index, row in performance_df.iterrows():
                metric = row.to_dict()
                
                # Ensure all fields are properly typed
                try:
                    metric['developer_id'] = int(metric['developer_id'])
                    metric['ticket_id'] = int(metric['ticket_id'])
                    metric['completion_time'] = float(metric['completion_time'])
                    metric['revisions'] = int(metric['revisions'])
                    metric['sentiment_score'] = float(metric['sentiment_score'])
                    self.performance_tracker.metrics.append(metric)
                except (ValueError, TypeError) as e:
                    print(f"Warning: Invalid performance data at index {index}: {e}")
        
            print(f"Loaded {len(self.performance_tracker.metrics)} performance records from performance_data_small.csv")
        except Exception as e:
            print(f"Warning: Could not load performance_data_small.csv: {e}")
            self.performance_tracker.metrics = []
    
    def _generate_sample_developers(self):
        # Fallback sample data
        self.developers = [
            {'id': 1, 'name': 'John', 'skills': ['python', 'frontend', 'ui'], 'availability': 40, 'current_workload': 0, 'experience_level': 4},
            {'id': 2, 'name': 'Mary', 'skills': ['python', 'backend', 'email'], 'availability': 40, 'current_workload': 0, 'experience_level': 5},
            {'id': 3, 'name': 'Jane', 'skills': ['python', 'backend', 'security'], 'availability': 40, 'current_workload': 0, 'experience_level': 3}
        ]
    
    def _generate_sample_tickets(self):
        # Fallback sample data
        features = [
            {
                "title": "User Authentication",
                "description": "Implement secure user authentication with OAuth and password reset functionality.",
                "priority": "high",
                "estimated_hours": 24
            },
            {
                "title": "Database Schema",
                "description": "Design and implement database schema for user profiles.",
                "priority": "medium",
                "estimated_hours": 16
            },
            {
                "title": "API Endpoints",
                "description": "Create REST API endpoints for user management.",
                "priority": "high",
                "estimated_hours": 20
            }
        ]
        
        for i, feature in enumerate(features, 1):
            ticket = self.ticket_gen.generate_ticket(feature)
            ticket['id'] = i
            self.tickets.append(ticket)
    
    def process_feature_story(self, feature_story):
        """Process a feature story and create a ticket."""
        # Use GPT simulation to generate detailed ticket
        ticket_data = self.gpt_simulation.generate_ticket_details(feature_story)
        
        # Add entities extracted from original description with error handling
        try:
            entities = self.nlp.extract_entities(feature_story['description'])
            ticket_data['entities'] = entities
        except Exception as e:
            print(f"Error extracting entities: {e}")
            # Provide a default entities structure
            ticket_data['entities'] = {
                'priorities': ['medium'],
                'dependencies': [],
                'deadlines': [],
                'tasks': []
            }
        
        # Find the highest existing ticket ID and increment by 1
        max_id = max([t['id'] for t in self.tickets], default=0)
        ticket_data['id'] = max_id + 1
        ticket_data['status'] = 'backlog'
        
        self.tickets.append(ticket_data)
        self.auto_save()
        return ticket_data
    
    def reset_ticket_ids(self):
        """Reset ticket IDs to start from 1 and update performance data"""
        # Sort tickets by current ID
        sorted_tickets = sorted(self.tickets, key=lambda x: x['id'])
        
        # Create a mapping from old ID to new ID
        id_mapping = {}
        for new_id, ticket in enumerate(sorted_tickets, 1):
            old_id = ticket['id']
            id_mapping[old_id] = new_id
            ticket['id'] = new_id
        
        # Update performance data
        for metric in self.performance_tracker.metrics:
            if metric['ticket_id'] in id_mapping:
                metric['ticket_id'] = id_mapping[metric['ticket_id']]
        
        # Save the updated data
        self.manual_save()
        
        return True
    
    def get_ticket_recommendations(self, ticket_id):
        """Get ticket recommendations with error handling"""
        ticket = next((t for t in self.tickets if t['id'] == ticket_id), None)
        if not ticket:
            raise NotFoundError("Ticket", ticket_id)
        
        # Get historical data
        historical_data = self.performance_tracker.get_historical_performance_data()
        
        # Try RL recommendation first
        rl_recommendation = self.rl_assignment.recommend_developer(ticket, self.developers)
        
        recommendations = []
        developer_ids = set()  # Track developer IDs to avoid duplicates
        
        if rl_recommendation:
            # Calculate match score for RL recommendation
            skill_match = self.rl_assignment._calculate_skill_match(ticket, rl_recommendation)
            availability_score = self.rl_assignment._calculate_availability_score(rl_recommendation)
            
            # Get historical performance
            dev_perf = historical_data.get(rl_recommendation['id'], {})
            
            recommendations.append({
                'developer_id': rl_recommendation['id'],
                'developer_name': rl_recommendation['name'],
                'match_score': (skill_match * 0.6) + (availability_score * 0.4),
                'skills_match': dev_perf,
                'method': 'RL'
            })
            developer_ids.add(rl_recommendation['id'])
        
        # Add traditional recommendations as backup
        traditional_recs = self.recommendation_engine.recommend_developers(ticket, self.developers, historical_data)
        
        # Add traditional recommendations, avoiding duplicates
        for rec in traditional_recs:
            if rec['developer_id'] not in developer_ids:
                recommendations.append(rec)
                developer_ids.add(rec['developer_id'])
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:3]  # Return top 3
    
    def estimate_ticket_timeline(self, ticket_id):
        ticket = next((t for t in self.tickets if t['id'] == ticket_id), None)
        if not ticket:
            return None
        
        # If ML models are trained, use them
        if self.training_module.is_trained:
            # We need a developer for ML estimation, so we'll use the first available or the one with the best match
            historical_data = self.performance_tracker.get_historical_performance_data()
            recommendations = self.recommendation_engine.recommend_developers(ticket, self.developers, historical_data)
            
            if recommendations:
                developer = next((d for d in self.developers if d['id'] == recommendations[0]['developer_id']), None)
                if developer:
                    return self.training_module.estimate_timeline(ticket, developer, historical_data)
        
        # Fall back to Monte Carlo estimation
        return self.monte_carlo.estimate_task_duration(ticket['estimated_hours'], ticket['complexity'])
    
    def assign_developer_to_ticket(self, ticket_id, developer_id=None):
        """Assign developer to ticket with error handling"""
        ticket = next((t for t in self.tickets if t['id'] == ticket_id), None)
        if not ticket:
            raise NotFoundError("Ticket", ticket_id)
        
        if ticket['status'] == 'completed':
            raise ConflictError("Cannot assign a completed ticket")
        
        if developer_id is None:
            # Get recommendations
            recommendations = self.get_ticket_recommendations(ticket_id)
            return recommendations
        
        developer = next((d for d in self.developers if d['id'] == developer_id), None)
        if not developer:
            raise NotFoundError("Developer", developer_id)
        
        # Check availability
        if developer['current_workload'] + ticket['estimated_hours'] > developer['availability']:
            raise ConflictError(f"Developer {developer['name']} doesn't have enough availability")
        
        # Use retry_operation for the assignment
        def perform_assignment():
            # If the ticket was previously assigned to someone else, reduce their workload
            if ticket.get('assigned_to') is not None and ticket['assigned_to'] != developer_id:
                prev_dev = next((d for d in self.developers if d['id'] == ticket['assigned_to']), None)
                if prev_dev:
                    prev_dev['current_workload'] -= ticket['estimated_hours']
            
            # Update ticket status to 'in_progress' when assigned
            ticket['status'] = 'in_progress'
            ticket['assigned_to'] = developer_id
            developer['current_workload'] += ticket['estimated_hours']
            self.auto_save()
            return True
        
        return retry_operation(perform_assignment, max_attempts=3)
    
    def complete_ticket(self, ticket_id, completion_time, revisions, sentiment_score):
        ticket = next((t for t in self.tickets if t['id'] == ticket_id), None)
        if not ticket:
            return False
        
        if ticket.get('assigned_to') is None:
            return False
        
        developer_id = ticket['assigned_to']
        # Update ticket status to 'completed' when completed
        ticket['status'] = 'completed'
        ticket['completion_time'] = completion_time
        
        # Track performance
        self.performance_tracker.track_performance(developer_id, ticket_id, completion_time, revisions, sentiment_score)
        
        # Save performance data to CSV
        self._save_performance_data_to_csv()
        
        developer = next((d for d in self.developers if d['id'] == developer_id), None)
        if developer:
            developer['current_workload'] -= ticket['estimated_hours']
        
        self.auto_save()
        return True
    
    def _save_performance_data_to_csv(self):
        """Save performance data to CSV file"""
        try:
            # Always write the entire performance data to the CSV
            with open('performance_data_small.csv', 'w', newline='') as csvfile:
                fieldnames = ['developer_id', 'ticket_id', 'completion_time', 'revisions', 'sentiment_score', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write all performance metrics
                for metric in self.performance_tracker.metrics:
                    writer.writerow({
                        'developer_id': metric['developer_id'],
                        'ticket_id': metric['ticket_id'],
                        'completion_time': metric['completion_time'],
                        'revisions': metric['revisions'],
                        'sentiment_score': metric['sentiment_score'],
                        'timestamp': metric['timestamp']
                    })
            
            print(f"Saved {len(self.performance_tracker.metrics)} performance records to CSV")
        except Exception as e:
            print(f"Error saving performance data to CSV: {e}")
    
    def get_system_status(self):
        total_tickets = len(self.tickets)
        completed_tickets = len([t for t in self.tickets if t['status'] == 'completed'])
        in_progress_tickets = len([t for t in self.tickets if t['status'] == 'in_progress'])
        backlog_tickets = len([t for t in self.tickets if t['status'] == 'backlog'])
        
        total_workload = sum(d['current_workload'] for d in self.developers)
        total_availability = sum(d['availability'] for d in self.developers)
        
        return {
            'total_tickets': total_tickets,
            'completed_tickets': completed_tickets,
            'in_progress_tickets': in_progress_tickets,
            'backlog_tickets': backlog_tickets,
            'total_workload': total_workload,
            'total_availability': total_availability,
            'utilization_rate': (total_workload / total_availability) * 100 if total_availability > 0 else 0
        }
    
    def get_developer_performance(self, developer_id):
        # Get performance data for this developer
        developer_metrics = [m for m in self.performance_tracker.metrics if m['developer_id'] == developer_id]
        
        if not developer_metrics:
            return None
        
        # Calculate metrics
        velocity = sum(m['completion_time'] for m in developer_metrics) / len(developer_metrics)
        
        total_revisions = sum(m['revisions'] for m in developer_metrics)
        accuracy = 1.0 / (1.0 + total_revisions * 0.1)
        
        avg_sentiment = sum(m['sentiment_score'] for m in developer_metrics) / len(developer_metrics)
        
        return {
            'metrics': developer_metrics,
            'average_completion_time': velocity,
            'accuracy': accuracy,
            'total_completed_tickets': len(developer_metrics),
            'average_sentiment': avg_sentiment,
            'historical_performance': {
                'velocity': velocity,
                'accuracy': accuracy,
                'sentiment': avg_sentiment,
                'tickets_completed': len(developer_metrics)
            }
        }
    
    def check_ml_status(self):
        """Check if ML models are trained and available"""
        if self.training_module.is_trained:
            print("ML models are trained and available for recommendations and estimations.")
            return True
        else:
            print("ML models are not trained. Using rule-based recommendations.")
            return False
    
    def auto_save(self):
        """Auto-save current system state to CSV files"""
        try:
            # Create backup of current files
            self._backup_data_files()
            
            # Save developers
            developers_data = []
            for dev in self.developers:
                dev_data = {
                    'id': dev['id'],
                    'name': dev['name'],
                    'skills': json.dumps(dev['skills']),  # Save as JSON string
                    'availability': dev['availability'],
                    'current_workload': dev['current_workload'],
                    'experience_level': dev['experience_level']
                }
                developers_data.append(dev_data)
            
            developers_df = pd.DataFrame(developers_data)
            developers_df.to_csv('developers_small.csv', index=False)
            
            # Save tickets
            tickets_data = []
            for ticket in self.tickets:
                ticket_data = {
                    'id': ticket['id'],
                    'title': ticket['title'],
                    'description': ticket['description'],
                    'priority': ticket['priority'],
                    'complexity': ticket['complexity'],
                    'estimated_hours': ticket['estimated_hours'],
                    'status': ticket['status'],
                    'tasks': ', '.join(ticket['tasks']),
                    'assigned_to': ticket.get('assigned_to', None)
                }
                tickets_data.append(ticket_data)
            
            tickets_df = pd.DataFrame(tickets_data)
            tickets_df.to_csv('sprint_documents_small.csv', index=False)
            
            # Save performance data
            self._save_performance_data_to_csv()
            
            print("Auto-saved data successfully.")
        except Exception as e:
            print(f"Error auto-saving data: {e}")
    
    def manual_save(self):
        """Manually save current system state to CSV files"""
        try:
            # Save developers
            developers_data = []
            for dev in self.developers:
                dev_data = {
                    'id': dev['id'],
                    'name': dev['name'],
                    'skills': json.dumps(dev['skills']),  # Save as JSON string
                    'availability': dev['availability'],
                    'current_workload': dev['current_workload'],
                    'experience_level': dev['experience_level']
                }
                developers_data.append(dev_data)
            
            developers_df = pd.DataFrame(developers_data)
            developers_df.to_csv('developers_small.csv', index=False)
            
            # Save tickets
            tickets_data = []
            for ticket in self.tickets:
                ticket_data = {
                    'id': ticket['id'],
                    'title': ticket['title'],
                    'description': ticket['description'],
                    'priority': ticket['priority'],
                    'complexity': ticket['complexity'],
                    'estimated_hours': ticket['estimated_hours'],
                    'status': ticket['status'],
                    'tasks': ', '.join(ticket['tasks']),
                    'assigned_to': ticket.get('assigned_to', None)
                }
                tickets_data.append(ticket_data)
            
            tickets_df = pd.DataFrame(tickets_data)
            tickets_df.to_csv('sprint_documents_small.csv', index=False)
            
            # Save performance data
            self._save_performance_data_to_csv()
            
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def _backup_data_files(self):
        """Create backup of current data files"""
        try:
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Backup developers file
            if os.path.exists('developers_small.csv'):
                shutil.copy('developers_small.csv', f'{backup_dir}/developers_small_{timestamp}.csv')
            
            # Backup tickets file
            if os.path.exists('sprint_documents_small.csv'):
                shutil.copy('sprint_documents_small.csv', f'{backup_dir}/sprint_documents_small_{timestamp}.csv')
            
            # Backup performance file
            if os.path.exists('performance_data_small.csv'):
                shutil.copy('performance_data_small.csv', f'{backup_dir}/performance_data_small_{timestamp}.csv')
            
        except Exception as e:
            print(f"Error creating backup: {e}")
    
    def save_data_to_csv(self):
        """Save current system state to CSV files (for backward compatibility)"""
        self.manual_save()
    
    def add_comment_to_ticket(self, ticket_id, developer_id, comment_text):
        """Add a comment to a ticket and analyze its sentiment"""
        ticket = next((t for t in self.tickets if t['id'] == ticket_id), None)
        if not ticket:
            return False
        
        # Analyze sentiment
        sentiment = self.nlp.analyze_sentiment(comment_text)
        
        # For now, just print the sentiment analysis
        # In a full implementation, you would save this to a database
        print(f"Comment sentiment: {sentiment['label']} (score: {sentiment['score']:.2f})")
        
        return True
    
    def export_ticket_to_jira(self, ticket_id):
        """Export a ticket to Jira"""
        ticket = next((t for t in self.tickets if t['id'] == ticket_id), None)
        if not ticket:
            return False
        
        if not self.jira_integration:
            print("Jira integration not configured")
            return False
        
        # Get assigned developer name
        assigned_to = None
        if ticket.get('assigned_to'):
            developer = next((d for d in self.developers if d['id'] == ticket['assigned_to']), None)
            if developer:
                assigned_to = developer['name'].lower().replace(' ', '.')
        
        ticket_data = {
            'title': ticket['title'],
            'description': ticket['description'],
            'priority': ticket['priority'],
            'estimated_hours': ticket['estimated_hours'],
            'assigned_to': assigned_to,
            'project_key': self.jira_config.get('project_key', 'SS')
        }
        
        result = self.jira_integration.create_ticket(ticket_data)
        
        if 'error' not in result:
            # Store Jira ID in ticket
            ticket['jira_id'] = result['key']
            self.auto_save()
            return True
        else:
            print(f"Error exporting to Jira: {result['error']}")
            return False
    
    def update_jira_ticket_status(self, ticket_id, status):
        """Update Jira ticket status"""
        ticket = next((t for t in self.tickets if t['id'] == ticket_id), None)
        if not ticket or not self.jira_integration or not ticket.get('jira_id'):
            return False
        
        return self.jira_integration.update_ticket_status(ticket['jira_id'], status)
    
    def optimize_workload(self):
        """Optimize workload distribution across developers"""
        historical_data = self.performance_tracker.get_historical_performance_data()
        assignments = self.workload_balancer.optimize_workload(self.tickets, self.developers, historical_data)
        
        # Apply assignments
        for assignment in assignments:
            ticket = next((t for t in self.tickets if t['id'] == assignment['ticket_id']), None)
            developer = next((d for d in self.developers if d['id'] == assignment['developer_id']), None)
            
            if ticket and developer:
                # Check if developer has enough availability
                if developer['current_workload'] + ticket['estimated_hours'] <= developer['availability']:
                    # Assign ticket to developer
                    if ticket.get('assigned_to') is not None and ticket['assigned_to'] != developer['id']:
                        # Reduce workload of previous developer
                        prev_dev = next((d for d in self.developers if d['id'] == ticket['assigned_to']), None)
                        if prev_dev:
                            prev_dev['current_workload'] -= ticket['estimated_hours']
                
                    ticket['assigned_to'] = developer['id']
                    ticket['status'] = 'in_progress'
                    developer['current_workload'] += ticket['estimated_hours']
        
        self.auto_save()
        return assignments
    
    def balance_workload(self):
        """Balance workload among developers"""
        historical_data = self.performance_tracker.get_historical_performance_data()
        return self.workload_balancer.balance_workload(self.developers, historical_data)
    
    def generate_progress_report(self):
        """Generate a comprehensive progress report"""
        historical_data = self.performance_tracker.get_historical_performance_data()
        return self.progress_monitor.generate_progress_report(self.tickets, self.developers, historical_data)
    
    def get_real_time_metrics(self):
        """Get real-time metrics for dashboard"""
        return self.progress_monitor.get_real_time_metrics(self.tickets, self.developers)
    
    def adjust_priorities_dynamically(self):
        """Adjust ticket priorities based on various factors"""
        adjustments = []
        
        # Get current system status
        status = self.get_system_status()
        utilization_rate = status['utilization_rate'] / 100  # Convert to decimal
        
        # Factor 1: Adjust based on system utilization
        if utilization_rate > 0.9:  # Very high utilization
            # Deprioritize medium and low priority tasks
            for ticket in self.tickets:
                if ticket['status'] == 'backlog' and ticket['priority'] in ['medium', 'low']:
                    old_priority = ticket['priority']
                    ticket['priority'] = 'low' if old_priority == 'medium' else 'low'
                    adjustments.append({
                        'ticket_id': ticket['id'],
                        'old_priority': old_priority,
                        'new_priority': ticket['priority'],
                        'reason': 'High system utilization'
                    })
        
        # Factor 2: Adjust based on deadline proximity
        today = datetime.datetime.now()
        for ticket in self.tickets:
            if ticket.get('deadline') and ticket['status'] != 'completed':
                deadline = datetime.datetime.fromisoformat(ticket['deadline'])
                days_to_deadline = (deadline - today).days
                
                if days_to_deadline <= 3 and ticket['priority'] != 'critical':
                    old_priority = ticket['priority']
                    ticket['priority'] = 'high' if old_priority != 'critical' else 'critical'
                    adjustments.append({
                        'ticket_id': ticket['id'],
                        'old_priority': old_priority,
                        'new_priority': ticket['priority'],
                        'reason': 'Approaching deadline'
                    })
        
        # Factor 3: Adjust based on dependency chain
        # Find tickets that are blocking many others
        for ticket in self.tickets:
            if ticket['status'] == 'backlog':
                blocking_count = 0
                for other_ticket in self.tickets:
                    if ticket['id'] in other_ticket.get('dependencies', []):
                        blocking_count += 1
                
                if blocking_count >= 3:  # If 3 or more tasks depend on this one
                    old_priority = ticket['priority']
                    ticket['priority'] = 'high' if old_priority != 'critical' else 'critical'
                    adjustments.append({
                        'ticket_id': ticket['id'],
                        'old_priority': old_priority,
                        'new_priority': ticket['priority'],
                        'reason': f'Blocking {blocking_count} other tasks'
                    })
        
        # Factor 4: Adjust based on developer availability
        for dev in self.developers:
            utilization = dev['current_workload'] / dev['availability'] if dev['availability'] > 0 else 0
            
            if utilization < 0.3:  # Underutilized developer
                # Increase priority of tasks that match this developer's skills
                dev_tickets = [t for t in self.tickets if t['status'] == 'backlog']
                
                # Sort by skill match
                dev_tickets.sort(key=lambda t: self._calculate_skill_match(t, dev), reverse=True)
                
                # Increase priority of top matching tasks
                for ticket in dev_tickets[:2]:  # Top 2 tasks
                    if ticket['priority'] == 'low':
                        old_priority = ticket['priority']
                        ticket['priority'] = 'medium'
                        adjustments.append({
                            'ticket_id': ticket['id'],
                            'old_priority': old_priority,
                            'new_priority': ticket['priority'],
                            'reason': f'Matches underutilized developer: {dev["name"]}'
                        })
        
        if adjustments:
            self.auto_save()
        
        return adjustments
    
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