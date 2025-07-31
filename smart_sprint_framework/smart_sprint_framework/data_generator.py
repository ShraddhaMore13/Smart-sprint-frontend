# data_generator.py
import csv
import random
import json
from datetime import datetime, timedelta

def generate_developers_csv():
    skills = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'swift',
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
        'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'git',
        'jenkins', 'ansible', 'puppet', 'chef', 'nagios', 'prometheus', 'grafana',
        'elasticsearch', 'kibana', 'splunk', 'jira', 'trello', 'asana', 'confluence'
    ]
    
    with open('developers.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'skills', 'availability', 'current_workload', 'experience_level'])
        
        for i in range(1, 101):
            num_skills = random.randint(3, 8)
            dev_skills = random.sample(skills, num_skills)
            
            first_names = ['John', 'Sarah', 'Mike', 'Emma', 'Alex', 'Lisa', 'David', 'Olivia', 'James', 'Sophia']
            last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson']
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            availability = random.randint(30, 45)
            if random.random() < 0.3:
                max_workload = min(30, int(availability * 0.8))
                if max_workload >= 5:
                    current_workload = random.randint(5, max_workload)
                else:
                    current_workload = 0
            else:
                current_workload = 0
            
            experience_level = random.randint(1, 5)
            
            writer.writerow([i, name, json.dumps(dev_skills), availability, current_workload, experience_level])

def generate_small_developers_csv():
    skills = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'swift',
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
        'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'git',
        'jenkins', 'ansible', 'puppet', 'chef', 'nagios', 'prometheus', 'grafana',
        'elasticsearch', 'kibana', 'splunk', 'jira', 'trello', 'asana', 'confluence'
    ]
    
    with open('developers_small.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'skills', 'availability', 'current_workload', 'experience_level'])
        
        for i in range(1, 11):  # Only 10 developers
            num_skills = random.randint(3, 8)
            dev_skills = random.sample(skills, num_skills)
            
            first_names = ['John', 'Sarah', 'Mike', 'Emma', 'Alex', 'Lisa', 'David', 'Olivia', 'James', 'Sophia']
            last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson']
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            availability = random.randint(30, 45)
            if random.random() < 0.3:
                max_workload = min(30, int(availability * 0.8))
                if max_workload >= 5:
                    current_workload = random.randint(5, max_workload)
                else:
                    current_workload = 0
            else:
                current_workload = 0
            
            experience_level = random.randint(1, 5)
            
            writer.writerow([i, name, json.dumps(dev_skills), availability, current_workload, experience_level])

def generate_sprint_documents_csv():
    priorities = ['low', 'medium', 'high', 'critical']
    features = [
        "User authentication with OAuth2",
        "Database schema design and implementation",
        "REST API endpoints for user management",
        "User dashboard with analytics",
        "Payment gateway integration",
        "Email notification system",
        "File upload and storage functionality",
        "Search functionality with filters",
        "User profile management",
        "Role-based access control",
        "Real-time chat feature",
        "Data export to CSV/PDF",
        "Mobile responsive design",
        "Performance monitoring and alerts",
        "Security audit and vulnerability fixes",
        "Internationalization support",
        "User feedback collection system",
        "Analytics dashboard for administrators",
        "Cache implementation for performance",
        "Logging and error tracking"
    ]
    
    with open('sprint_documents.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'description', 'priority', 'estimated_hours', 'complexity', 'dependencies'])
        
        for i in range(1, 101):
            feature = random.choice(features)
            
            if 'authentication' in feature.lower():
                description = f"Implement secure user authentication system with OAuth2 integration. Include password reset functionality and session management. This feature depends on database setup being complete."
            elif 'database' in feature.lower():
                description = f"Design and implement database schema for {feature.lower().replace('database schema design and implementation', 'the application').replace('database', 'the application')}. Include proper indexing and relationships. Normal priority task."
            elif 'api' in feature.lower():
                description = f"Create REST API endpoints for {feature.lower().replace('rest api endpoints for', '').replace('api', 'API functionality')}. Include proper authentication and error handling. High priority task."
            elif 'dashboard' in feature.lower():
                description = f"Develop user dashboard with analytics and visualization. Include real-time updates and filtering capabilities. Medium priority task."
            else:
                description = f"Implement {feature.lower()}. Include proper error handling and documentation. Medium priority task."
            
            priority = random.choice(priorities)
            estimated_hours = random.randint(8, 40)
            complexity = min(5, max(1, estimated_hours // 8))
            
            dependencies = []
            # Only generate dependencies if i > 1 (no dependencies for the first ticket)
            if i > 1 and random.random() < 0.4:
                dependency_count = random.randint(1, min(2, i-1))  # Ensure we don't exceed available tickets
                for _ in range(dependency_count):
                    dep_id = random.randint(1, i-1)
                    dependencies.append(str(dep_id))
            
            writer.writerow([i, feature, description, priority, estimated_hours, complexity, ','.join(dependencies)])

def generate_small_sprint_documents_csv():
    # Define 15 specific tickets with different tasks
    tickets = [
        {
            "id": 1,
            "title": "Security audit and vulnerability fixes",
            "description": "Conduct a comprehensive security audit of the application and implement fixes for identified vulnerabilities.",
            "priority": "critical",
            "estimated_hours": 31.0,
            "complexity": 1,
            "dependencies": ""
        },
        {
            "id": 2,
            "title": "Logging and error tracking",
            "description": "Implement comprehensive logging and error tracking system for monitoring application health.",
            "priority": "critical",
            "estimated_hours": 10.0,
            "complexity": 1,
            "dependencies": ""
        },
        {
            "id": 3,
            "title": "Database schema design and implementation",
            "description": "Design and implement efficient database schema for the application with proper relationships.",
            "priority": "medium",
            "estimated_hours": 22.0,
            "complexity": 1,
            "dependencies": ""
        },
        {
            "id": 4,
            "title": "User authentication with OAuth2",
            "description": "Implement secure user authentication system using OAuth2 protocol.",
            "priority": "high",
            "estimated_hours": 18.0,
            "complexity": 2,
            "dependencies": ""
        },
        {
            "id": 5,
            "title": "REST API endpoints for user management",
            "description": "Create RESTful API endpoints for managing user accounts and profiles.",
            "priority": "high",
            "estimated_hours": 24.0,
            "complexity": 2,
            "dependencies": "4"
        },
        {
            "id": 6,
            "title": "User dashboard with analytics",
            "description": "Develop user dashboard with data visualization and analytics features.",
            "priority": "medium",
            "estimated_hours": 28.0,
            "complexity": 3,
            "dependencies": "4,5"
        },
        {
            "id": 7,
            "title": "Payment gateway integration",
            "description": "Integrate third-party payment gateway for processing transactions.",
            "priority": "high",
            "estimated_hours": 32.0,
            "complexity": 4,
            "dependencies": "4,5"
        },
        {
            "id": 8,
            "title": "Email notification system",
            "description": "Implement email notification system for user alerts and system notifications.",
            "priority": "medium",
            "estimated_hours": 16.0,
            "complexity": 2,
            "dependencies": ""
        },
        {
            "id": 9,
            "title": "File upload and storage functionality",
            "description": "Implement secure file upload and storage system with proper validation.",
            "priority": "medium",
            "estimated_hours": 20.0,
            "complexity": 3,
            "dependencies": ""
        },
        {
            "id": 10,
            "title": "Search functionality with filters",
            "description": "Create advanced search functionality with multiple filter options.",
            "priority": "medium",
            "estimated_hours": 18.0,
            "complexity": 3,
            "dependencies": "3"
        },
        {
            "id": 11,
            "title": "User profile management",
            "description": "Develop user profile management system with privacy settings.",
            "priority": "medium",
            "estimated_hours": 14.0,
            "complexity": 2,
            "dependencies": "4,5"
        },
        {
            "id": 12,
            "title": "Role-based access control",
            "description": "Implement role-based access control system for securing application features.",
            "priority": "high",
            "estimated_hours": 26.0,
            "complexity": 4,
            "dependencies": "4"
        },
        {
            "id": 13,
            "title": "Real-time chat feature",
            "description": "Develop real-time chat functionality using WebSockets.",
            "priority": "low",
            "estimated_hours": 30.0,
            "complexity": 5,
            "dependencies": "4,5"
        },
        {
            "id": 14,
            "title": "Data export to CSV/PDF",
            "description": "Implement functionality to export data in CSV and PDF formats.",
            "priority": "low",
            "estimated_hours": 12.0,
            "complexity": 2,
            "dependencies": ""
        },
        {
            "id": 15,
            "title": "Mobile responsive design",
            "description": "Ensure all application components are fully responsive for mobile devices.",
            "priority": "medium",
            "estimated_hours": 24.0,
            "complexity": 3,
            "dependencies": ""
        }
    ]
    
    with open('sprint_documents_small.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'description', 'priority', 'estimated_hours', 'complexity', 'dependencies'])
        
        for ticket in tickets:
            writer.writerow([
                ticket['id'],
                ticket['title'],
                ticket['description'],
                ticket['priority'],
                ticket['estimated_hours'],
                ticket['complexity'],
                ticket['dependencies']
            ])

def generate_performance_data():
    with open('performance_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['developer_id', 'ticket_id', 'completion_time', 'revisions', 'sentiment_score'])
        
        for dev_id in range(1, 101):
            ticket_count = random.randint(5, 20)
            
            for ticket_id in range(1, ticket_count + 1):
                base_time = random.randint(5, 30)
                completion_time = round(base_time * random.uniform(0.7, 1.5), 1)
                
                complexity_factor = random.randint(1, 5)
                experience_factor = random.randint(1, 5)
                revisions = max(0, random.randint(0, complexity_factor + 6 - experience_factor))
                
                experience_boost = experience_factor * 0.1
                workload_penalty = min(0.3, (dev_id % 10) * 0.03)
                sentiment_score = round(min(1.0, max(0.5, 0.7 + experience_boost - workload_penalty)), 2)
                
                writer.writerow([dev_id, ticket_id, completion_time, revisions, sentiment_score])

def generate_small_performance_data():
    with open('performance_data_small.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['developer_id', 'ticket_id', 'completion_time', 'revisions', 'sentiment_score'])
        
        for dev_id in range(1, 11):  # Only 10 developers
            ticket_count = random.randint(3, 8)  # Each developer completed 3-8 tickets
            
            for i in range(1, ticket_count + 1):
                ticket_id = random.randint(1, 15)  # Only 15 tickets
                base_time = random.randint(5, 30)
                completion_time = round(base_time * random.uniform(0.7, 1.5), 1)
                
                complexity_factor = random.randint(1, 5)
                experience_factor = random.randint(1, 5)
                revisions = max(0, random.randint(0, complexity_factor + 6 - experience_factor))
                
                experience_boost = experience_factor * 0.1
                workload_penalty = min(0.3, (dev_id % 10) * 0.03)
                sentiment_score = round(min(1.0, max(0.5, 0.7 + experience_boost - workload_penalty)), 2)
                
                writer.writerow([dev_id, ticket_id, completion_time, revisions, sentiment_score])

def generate_all_data():
    print("Generating developers data...")
    generate_developers_csv()
    print("Generating small developers data...")
    generate_small_developers_csv()
    print("Generating sprint documents...")
    generate_sprint_documents_csv()
    print("Generating small sprint documents...")
    generate_small_sprint_documents_csv()
    print("Generating performance data...")
    generate_performance_data()
    print("Generating small performance data...")
    generate_small_performance_data()
    print("CSV files generated successfully!")

if __name__ == "__main__":
    generate_all_data()