import re
import random

class GPTSimulation:
    def __init__(self):
        self.task_templates = {
            "authentication": [
                "Design authentication flow",
                "Implement login functionality",
                "Create user session management",
                "Add password reset feature",
                "Implement OAuth integration"
            ],
            "database": [
                "Design database schema",
                "Implement data models",
                "Create database migrations",
                "Set up database indexes",
                "Implement data validation"
            ],
            "api": [
                "Design API endpoints",
                "Implement request handling",
                "Create API documentation",
                "Add input validation",
                "Implement error handling"
            ],
            "frontend": [
                "Design UI components",
                "Implement responsive layout",
                "Create user interactions",
                "Add animations",
                "Optimize performance"
            ],
            "backend": [
                "Design server architecture",
                "Implement business logic",
                "Create data processing",
                "Add security measures",
                "Optimize performance"
            ],
            "security": [
                "Conduct security audit",
                "Implement encryption",
                "Add authentication middleware",
                "Create access control",
                "Implement rate limiting"
            ],
            "testing": [
                "Write unit tests",
                "Create integration tests",
                "Implement test automation",
                "Add performance testing",
                "Create test documentation"
            ],
            "documentation": [
                "Write technical documentation",
                "Create user guides",
                "Add API documentation",
                "Create code comments",
                "Maintain changelog"
            ]
        }
    
    def generate_ticket_details(self, feature_story):
        """Generate detailed ticket information using simulated GPT-4"""
        title = feature_story['title']
        description = feature_story['description']
        priority = feature_story['priority']
        
        # Extract keywords from title and description
        text = f"{title} {description}".lower()
        
        # Determine ticket type based on keywords
        ticket_type = "general"
        for t in self.task_templates:
            if t in text:
                ticket_type = t
                break
        
        # Generate tasks based on ticket type
        if ticket_type in self.task_templates:
            tasks = self.task_templates[ticket_type].copy()
        else:
            tasks = [
                "Analyze requirements",
                "Design solution",
                "Implement core functionality",
                "Test implementation",
                "Document solution"
            ]
        
        # Customize tasks based on specific keywords
        if "password" in text and "reset" in text:
            tasks = [
                "Design password reset flow",
                "Implement password reset request",
                "Create secure token generation",
                "Implement email notification",
                "Develop password update page",
                "Test password reset functionality"
            ]
        elif "user" in text and "profile" in text:
            tasks = [
                "Design profile page layout",
                "Implement profile data retrieval",
                "Create profile update functionality",
                "Add profile image upload",
                "Implement privacy settings",
                "Test profile management"
            ]
        
        # Generate detailed description
        detailed_description = f"## Overview\n{description}\n\n## Requirements\n"
        
        # Add specific requirements based on ticket type
        if ticket_type == "authentication":
            detailed_description += "- Secure user authentication\n- Session management\n- Password encryption\n"
        elif ticket_type == "database":
            detailed_description += "- Efficient data storage\n- Data integrity\n- Performance optimization\n"
        elif ticket_type == "api":
            detailed_description += "- RESTful design\n- Proper error handling\n- Input validation\n"
        elif ticket_type == "frontend":
            detailed_description += "- Responsive design\n- Cross-browser compatibility\n- Accessibility\n"
        elif ticket_type == "backend":
            detailed_description += "- Scalable architecture\n- Error handling\n- Security measures\n"
        
        detailed_description += "\n## Acceptance Criteria\n"
        for i, task in enumerate(tasks, 1):
            detailed_description += f"{i}. {task}\n"
        
        # Estimate complexity based on description length and priority
        complexity = 1
        if len(description) > 200:
            complexity += 1
        if priority == "high":
            complexity += 1
        elif priority == "critical":
            complexity += 2
        
        complexity = min(5, complexity)
        
        # Estimate hours based on complexity and task count
        base_hours = complexity * 4
        task_hours = len(tasks) * 2
        estimated_hours = base_hours + task_hours
        
        # Add some randomness
        estimated_hours = int(estimated_hours * random.uniform(0.9, 1.1))
        
        return {
            'title': title,
            'description': detailed_description,
            'priority': priority,
            'complexity': complexity,
            'estimated_hours': estimated_hours,
            'tasks': tasks
        }
    
    def generate_subtasks(self, task_description):
        """Generate subtasks for a given task description"""
        # Simple rule-based subtask generation
        subtasks = []
        
        if "implement" in task_description.lower():
            subtasks.append("Research implementation approach")
            subtasks.append("Write code")
            subtasks.append("Test implementation")
            subtasks.append("Code review")
        
        if "design" in task_description.lower():
            subtasks.append("Create design mockups")
            subtasks.append("Review design with team")
            subtasks.append("Finalize design")
        
        if "test" in task_description.lower():
            subtasks.append("Write test cases")
            subtasks.append("Execute tests")
            subtasks.append("Document results")
        
        if not subtasks:
            subtasks = [
                "Analyze requirements",
                "Implement solution",
                "Test implementation",
                "Document results"
            ]
        
        return subtasks