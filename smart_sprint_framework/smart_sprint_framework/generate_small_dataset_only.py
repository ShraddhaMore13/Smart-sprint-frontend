import pandas as pd

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
    tickets_data = [
        {
            "id": 22,
            "title": "Test password reset functionality",
            "description": "Implement and test password reset functionality for the application.",
            "priority": "medium",
            "estimated_hours": 4.0,
            "complexity": 1,
            "status": "backlog",
            "tasks": "Design password reset flow, Implement password reset request form, Create secure token generation, Implement email notification system, Develop password update page, Test password reset functionality",
            "assigned_to": None
        },
        {
            "id": 23,
            "title": "Add login page",
            "description": "Create a user login page with authentication.",
            "priority": "medium",
            "estimated_hours": 8.0,
            "complexity": 3,
            "status": "backlog",
            "tasks": "Design login form, Implement authentication logic, Create session management, Develop logout functionality, Test authentication flow",
            "assigned_to": None
        },
        {
            "id": 24,
            "title": "Implement user authentication",
            "description": "Implement secure user authentication system.",
            "priority": "high",
            "estimated_hours": 10.0,
            "complexity": 4,
            "status": "backlog",
            "tasks": "Design authentication architecture, Implement OAuth2 integration, Create session management, Develop password reset functionality, Test authentication security",
            "assigned_to": None
        },
        {
            "id": 25,
            "title": "Create user registration",
            "description": "Develop user registration functionality.",
            "priority": "medium",
            "estimated_hours": 12.0,
            "complexity": 3,
            "status": "backlog",
            "tasks": "Design registration form, Implement user registration logic, Create email verification system, Develop registration confirmation page, Test registration process",
            "assigned_to": None
        },
        {
            "id": 26,
            "title": "Design user profile",
            "description": "Create user profile management system.",
            "priority": "medium",
            "estimated_hours": 14.0,
            "complexity": 3,
            "status": "backlog",
            "tasks": "Design profile page, Implement profile updates, Add profile picture upload, Create privacy settings, Test profile functionality",
            "assigned_to": None
        },
        {
            "id": 27,
            "title": "Implement role-based access",
            "description": "Develop role-based access control system.",
            "priority": "high",
            "estimated_hours": 16.0,
            "complexity": 4,
            "status": "backlog",
            "tasks": "Design permission system, Implement role management, Create access control UI, Add permission inheritance, Test access security",
            "assigned_to": None
        }
    ]
    
    tickets_df = pd.DataFrame(tickets_data)
    tickets_df.to_csv('sprint_documents_small.csv', index=False)
    print("Generated sprint_documents_small.csv with 6 unique tickets")

def generate_small_performance_data():
    import random
    
    performance_data = []
    
    # Generate some sample performance data
    for dev_id in range(1, 11):
        # Each developer has completed 3-8 tickets
        ticket_count = random.randint(3, 8)
        
        for i in range(1, ticket_count + 1):
            ticket_id = random.randint(22, 27)  # Only our 6 tickets
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
    print("Generated performance_data_small.csv")

def main():
    print("Generating small dataset...")
    generate_small_developers_csv()
    generate_small_sprint_documents_csv()
    generate_small_performance_data()
    print("Small dataset generation completed.")

if __name__ == "__main__":
    main()