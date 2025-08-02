import pandas as pd
import numpy as np
import random
from datetime import datetime

def generate_small_developers_csv():
    developers_data = [
        {'id': 1, 'name': 'John Smith', 'skills': '["python", "react", "mysql", "docker"]', 'availability': 40, 'current_workload': 0, 'experience_level': 4},
        {'id': 2, 'name': 'Sarah Johnson', 'skills': '["redis", "git", "mysql", "jenkins"]', 'availability': 40, 'current_workload': 0, 'experience_level': 1},
        {'id': 3, 'name': 'Mike Williams', 'skills': '["java", "spring", "postgresql", "docker"]', 'availability': 40, 'current_workload': 0, 'experience_level': 3},
        {'id': 4, 'name': 'Emma Davis', 'skills': '["javascript", "react", "node.js", "mongodb"]', 'availability': 40, 'current_workload': 0, 'experience_level': 4},
        {'id': 5, 'name': 'Alex Miller', 'skills': '["python", "django", "postgresql", "redis"]', 'availability': 40, 'current_workload': 0, 'experience_level': 5},
        {'id': 6, 'name': 'Lisa Brown', 'skills': '["java", "spring", "mysql", "kubernetes"]', 'availability': 40, 'current_workload': 0, 'experience_level': 3},
        {'id': 7, 'name': 'David Wilson', 'skills': '["typescript", "angular", "node.js", "mongodb"]', 'availability': 40, 'current_workload': 0, 'experience_level': 4},
        {'id': 8, 'name': 'Olivia Taylor', 'skills': '["python", "flask", "sqlite", "docker"]', 'availability': 40, 'current_workload': 0, 'experience_level': 2},
        {'id': 9, 'name': 'James Garcia', 'skills': '["c#", ".net", "sql server", "azure"]', 'availability': 40, 'current_workload': 0, 'experience_level': 4},
        {'id': 10, 'name': 'Sophia Rodriguez', 'skills': '["php", "laravel", "mysql", "aws"]', 'availability': 40, 'current_workload': 0, 'experience_level': 3}
    ]
    
    developers_df = pd.DataFrame(developers_data)
    developers_df.to_csv('developers_small.csv', index=False)
    print("Generated developers_small.csv")

def generate_small_sprint_documents_csv():
    # Define ticket templates with various types of work
    ticket_templates = [
        {
            "title": "Implement user authentication",
            "description": "Implement secure user authentication with OAuth and password reset functionality.",
            "priority": "high",
            "estimated_hours": 24.0,
            "complexity": 4
        },
        {
            "title": "Design database schema",
            "description": "Design and implement database schema for user profiles.",
            "priority": "medium",
            "estimated_hours": 16.0,
            "complexity": 3
        },
        {
            "title": "Create API endpoints",
            "description": "Create REST API endpoints for user management.",
            "priority": "high",
            "estimated_hours": 20.0,
            "complexity": 3
        },
        {
            "title": "Develop user dashboard",
            "description": "Develop user dashboard with analytics and visualization.",
            "priority": "medium",
            "estimated_hours": 28.0,
            "complexity": 4
        },
        {
            "title": "Implement payment gateway",
            "description": "Integrate third-party payment gateway for processing transactions.",
            "priority": "high",
            "estimated_hours": 32.0,
            "complexity": 5
        },
        {
            "title": "Add email notifications",
            "description": "Implement email notification system for user alerts and system notifications.",
            "priority": "medium",
            "estimated_hours": 16.0,
            "complexity": 3
        },
        {
            "title": "File upload functionality",
            "description": "Implement secure file upload and storage system with proper validation.",
            "priority": "medium",
            "estimated_hours": 20.0,
            "complexity": 3
        },
        {
            "title": "Search functionality",
            "description": "Create advanced search functionality with multiple filter options.",
            "priority": "medium",
            "estimated_hours": 18.0,
            "complexity": 3
        },
        {
            "title": "User profile management",
            "description": "Develop user profile management system with privacy settings.",
            "priority": "medium",
            "estimated_hours": 14.0,
            "complexity": 3
        },
        {
            "title": "Role-based access control",
            "description": "Implement role-based access control system for securing application features.",
            "priority": "high",
            "estimated_hours": 26.0,
            "complexity": 4
        },
        {
            "title": "Real-time chat feature",
            "description": "Implement real-time chat functionality using WebSockets.",
            "priority": "low",
            "estimated_hours": 30.0,
            "complexity": 5
        },
        {
            "title": "Data export functionality",
            "description": "Implement functionality to export data in CSV and PDF formats.",
            "priority": "low",
            "estimated_hours": 12.0,
            "complexity": 2
        },
        {
            "title": "Mobile responsive design",
            "description": "Ensure all application components are fully responsive for mobile devices.",
            "priority": "medium",
            "estimated_hours": 24.0,
            "complexity": 3
        },
        {
            "title": "Performance optimization",
            "description": "Optimize application performance for better user experience.",
            "priority": "medium",
            "estimated_hours": 20.0,
            "complexity": 4
        },
        {
            "title": "Security audit",
            "description": "Conduct comprehensive security audit and implement necessary fixes.",
            "priority": "high",
            "estimated_hours": 28.0,
            "complexity": 5
        },
        {
            "title": "Implement caching",
            "description": "Implement caching mechanism to improve application performance.",
            "priority": "medium",
            "estimated_hours": 16.0,
            "complexity": 3
        },
        {
            "title": "Create admin panel",
            "description": "Develop admin panel for system management and monitoring.",
            "priority": "medium",
            "estimated_hours": 22.0,
            "complexity": 4
        },
        {
            "title": "Add reporting feature",
            "description": "Implement reporting feature for generating various reports.",
            "priority": "low",
            "estimated_hours": 18.0,
            "complexity": 3
        },
        {
            "title": "Implement logging system",
            "description": "Implement comprehensive logging system for debugging and monitoring.",
            "priority": "medium",
            "estimated_hours": 14.0,
            "complexity": 2
        },
        {
            "title": "Create backup system",
            "description": "Implement automated backup system for data protection.",
            "priority": "high",
            "estimated_hours": 20.0,
            "complexity": 4
        },
        {
            "title": "Implement user registration",
            "description": "Develop user registration functionality with email verification.",
            "priority": "medium",
            "estimated_hours": 18.0,
            "complexity": 3
        },
        {
            "title": "Add password reset",
            "description": "Implement secure password reset functionality with email notifications.",
            "priority": "medium",
            "estimated_hours": 12.0,
            "complexity": 2
        },
        {
            "title": "Create login page",
            "description": "Design and implement user login page with authentication.",
            "priority": "medium",
            "estimated_hours": 10.0,
            "complexity": 2
        },
        {
            "title": "Implement session management",
            "description": "Create secure session management system for user authentication.",
            "priority": "high",
            "estimated_hours": 16.0,
            "complexity": 4
        },
        {
            "title": "Add two-factor authentication",
            "description": "Implement two-factor authentication for enhanced security.",
            "priority": "medium",
            "estimated_hours": 20.0,
            "complexity": 4
        },
        {
            "title": "Create user settings page",
            "description": "Develop user settings page for profile management.",
            "priority": "low",
            "estimated_hours": 12.0,
            "complexity": 2
        },
        {
            "title": "Implement data validation",
            "description": "Add comprehensive data validation for all user inputs.",
            "priority": "medium",
            "estimated_hours": 14.0,
            "complexity": 3
        },
        {
            "title": "Create error handling",
            "description": "Implement robust error handling throughout the application.",
            "priority": "medium",
            "estimated_hours": 16.0,
            "complexity": 3
        },
        {
            "title": "Add unit tests",
            "description": "Write comprehensive unit tests for core functionality.",
            "priority": "medium",
            "estimated_hours": 22.0,
            "complexity": 3
        },
        {
            "title": "Implement API rate limiting",
            "description": "Add rate limiting to API endpoints to prevent abuse.",
            "priority": "medium",
            "estimated_hours": 10.0,
            "complexity": 2
        },
        {
            "title": "Create documentation",
            "description": "Write comprehensive documentation for the application.",
            "priority": "low",
            "estimated_hours": 18.0,
            "complexity": 2
        },
        {
            "title": "Implement search filters",
            "description": "Add advanced filtering options to the search functionality.",
            "priority": "low",
            "estimated_hours": 12.0,
            "complexity": 2
        },
        {
            "title": "Add data analytics",
            "description": "Implement data analytics features for the dashboard.",
            "priority": "medium",
            "estimated_hours": 24.0,
            "complexity": 4
        },
        {
            "title": "Create notification system",
            "description": "Implement in-app notification system for user alerts.",
            "priority": "medium",
            "estimated_hours": 16.0,
            "complexity": 3
        },
        {
            "title": "Add dark mode",
            "description": "Implement dark mode theme for the application.",
            "priority": "low",
            "estimated_hours": 8.0,
            "complexity": 1
        },
        {
            "title": "Implement data encryption",
            "description": "Add encryption for sensitive data storage.",
            "priority": "high",
            "estimated_hours": 18.0,
            "complexity": 4
        },
        {
            "title": "Create user activity log",
            "description": "Implement user activity logging for security monitoring.",
            "priority": "medium",
            "estimated_hours": 14.0,
            "complexity": 3
        },
        {
            "title": "Add bulk operations",
            "description": "Implement bulk operations for data management.",
            "priority": "low",
            "estimated_hours": 12.0,
            "complexity": 2
        },
        {
            "title": "Implement data import",
            "description": "Add functionality to import data from CSV files.",
            "priority": "medium",
            "estimated_hours": 16.0,
            "complexity": 3
        },
        {
            "title": "Create help center",
            "description": "Develop help center with FAQs and tutorials.",
            "priority": "low",
            "estimated_hours": 20.0,
            "complexity": 2
        }
    ]
    
    tickets_data = []
    
    # Generate 35 tickets by cycling through the templates
    for i in range(1, 36):  # IDs from 1 to 35
        template = ticket_templates[i % len(ticket_templates)]
        
        # Add some variation to the estimated hours
        estimated_hours = template["estimated_hours"] * random.uniform(0.8, 1.2)
        
        # Randomly assign some tickets to developers
        assigned_to = random.choice([None, random.randint(1, 10)]) if random.random() < 0.3 else None
        
        # Randomly set some tickets to completed or in progress
        status_options = ["backlog", "in_progress", "completed"]
        status_weights = [0.7, 0.2, 0.1]  # 70% backlog, 20% in progress, 10% completed
        status = random.choices(status_options, weights=status_weights)[0]
        
        ticket_data = {
            "id": i,  # IDs start from 1
            "title": template["title"],
            "description": template["description"],
            "priority": template["priority"],
            "estimated_hours": round(estimated_hours, 1),
            "complexity": template["complexity"],
            "status": status,
            "tasks": "Analyze requirements, Design solution, Implement core functionality, Test implementation, Document solution",
            "assigned_to": assigned_to
        }
        tickets_data.append(ticket_data)
    
    tickets_df = pd.DataFrame(tickets_data)
    tickets_df.to_csv('sprint_documents_small.csv', index=False)
    print(f"Generated sprint_documents_small.csv with {len(tickets_data)} tickets")

def generate_small_performance_data():
    performance_data = []
    
    # Generate performance data for completed tickets
    for dev_id in range(1, 11):  # 10 developers
        # Each developer has completed 3-8 tickets
        ticket_count = random.randint(3, 8)
        
        for i in range(1, ticket_count + 1):
            # Only generate performance data for completed tickets
            # We'll assume tickets 1-12 are completed for this example (about 1/3 of 35)
            ticket_id = random.randint(1, 12)
            
            base_time = random.randint(5, 30)
            completion_time = round(base_time * random.uniform(0.7, 1.5), 1)
            
            complexity_factor = random.randint(1, 5)
            experience_factor = random.randint(1, 5)
            revisions = max(0, random.randint(0, complexity_factor + 6 - experience_factor))
            
            experience_boost = experience_factor * 0.1
            workload_penalty = min(0.3, (dev_id % 10) * 0.03)
            sentiment_score = round(min(1.0, max(0.5, 0.7 + experience_boost - workload_penalty)), 2)
            
            performance_data.append({
                'developer_id': dev_id,
                'ticket_id': ticket_id,
                'completion_time': completion_time,
                'revisions': revisions,
                'sentiment_score': sentiment_score
            })
    
    performance_df = pd.DataFrame(performance_data)
    performance_df.to_csv('performance_data_small.csv', index=False)
    print(f"Generated performance_data_small.csv with {len(performance_data)} records")

def main():
    print("Generating small dataset...")
    generate_small_developers_csv()
    generate_small_sprint_documents_csv()
    generate_small_performance_data()
    print("Small dataset generation completed.")

if __name__ == "__main__":
    main()