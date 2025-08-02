from flask import Flask, jsonify, request, send_from_directory
import os
import pandas as pd
import numpy as np
import traceback
from smart_sprint_system import SmartSprintSystem
from nlp_pipeline import NLPPipeline
from sprint_document_processor import SprintDocumentProcessor
from auth import login_required, admin_required, verify_password, generate_token
from error_handler import (
    handle_errors, ValidationError, AuthenticationError, 
    AuthorizationError, NotFoundError, ConflictError,
    validate_required_fields, validate_field_types, validate_positive_numbers
)
from dashboard_data import DashboardDataGenerator

app = Flask(__name__)

# Initialize the system
system = SmartSprintSystem()
nlp = NLPPipeline()
sprint_processor = SprintDocumentProcessor()

# In-memory user storage (in production, use a database)
users = {
    "admin": {
        "password": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
        "role": "admin"
    },
    "user": {
        "password": "793860fa51408bd7a5d3b4a518e5e8a9b7a5d3f5a5c5e5d5f5a5d5c5e5d5f5a5d5",
        "role": "user"
    }
}

@app.route('/api/login', methods=['POST'])
@handle_errors
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        raise ValidationError("Username and password are required")
    
    if verify_password(username, password):
        token = generate_token(username)
        response = jsonify({
            "token": token,
            "username": username,
            "role": users[username]["role"]
        })
        return response
    else:
        raise AuthenticationError("Invalid username or password")

@app.route('/api/tickets', methods=['GET'])
@handle_errors
@login_required
def get_tickets():
    tickets = system.tickets
    return jsonify(tickets)

@app.route('/api/tickets', methods=['POST'])
@handle_errors
@login_required
def create_ticket():
    data = request.json
    
    # Validate input
    validate_required_fields(data, ['title', 'description', 'priority', 'estimated_hours'])
    validate_field_types(data, {
        'title': str,
        'description': str,
        'priority': str,
        'estimated_hours': (int, float)
    })
    validate_positive_numbers(data, ['estimated_hours'])
    
    # Validate priority value
    if data['priority'] not in ['low', 'medium', 'high', 'critical']:
        raise ValidationError("Priority must be one of: low, medium, high, critical")
    
    ticket = system.process_feature_story(data)
    return jsonify(ticket), 201

@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
@handle_errors
@login_required
def get_ticket(ticket_id):
    ticket = next((t for t in system.tickets if t['id'] == ticket_id), None)
    if not ticket:
        raise NotFoundError("Ticket", ticket_id)
    return jsonify(ticket)

@app.route('/api/tickets/<int:ticket_id>/recommendations', methods=['GET'])
@handle_errors
@login_required
def get_recommendations(ticket_id):
    recommendations = system.get_ticket_recommendations(ticket_id)
    return jsonify(recommendations)

@app.route('/api/tickets/<int:ticket_id>/assign', methods=['POST'])
@handle_errors
@login_required
def assign_ticket(ticket_id):
    data = request.json
    developer_id = data.get('developer_id')
    
    if developer_id is None:
        # Get recommendations
        result = system.assign_developer_to_ticket(ticket_id)
        return jsonify(result)
    else:
        # Validate developer_id
        if not isinstance(developer_id, int) or developer_id <= 0:
            raise ValidationError("developer_id must be a positive integer")
        
        # Assign to specific developer
        success = system.assign_developer_to_ticket(ticket_id, developer_id)
        if not success:
            raise ConflictError("Assignment failed. Developer may not have enough availability.")
        return jsonify({'success': True})

@app.route('/api/tickets/<int:ticket_id>/complete', methods=['POST'])
@handle_errors
@login_required
def complete_ticket(ticket_id):
    data = request.json
    success = system.complete_ticket(
        ticket_id,
        data.get('completion_time'),
        data.get('revisions'),
        data.get('sentiment_score')
    )
    if success:
        return jsonify({'success': True})
    raise ConflictError("Completion failed. Check if ticket exists and is assigned.")

@app.route('/api/developers', methods=['GET'])
@handle_errors
@login_required
def get_developers():
    developers = system.developers
    return jsonify(developers)

@app.route('/api/developers/<int:developer_id>/performance', methods=['GET'])
@handle_errors
@login_required
def get_developer_performance(developer_id):
    performance = system.get_developer_performance(developer_id)
    if performance:
        return jsonify(performance)
    raise NotFoundError("Developer performance data", developer_id)

@app.route('/api/system/status', methods=['GET'])
@handle_errors
@login_required
def get_system_status():
    status = system.get_system_status()
    return jsonify(status)

@app.route('/api/system/save', methods=['POST'])
@handle_errors
@login_required
def save_system():
    try:
        system.manual_save()
        return jsonify({'success': True})
    except Exception as e:
        raise ConflictError(str(e))

@app.route('/api/nlp/analyze', methods=['POST'])
@handle_errors
@login_required
def analyze_text():
    data = request.json
    text = data.get('text', '')
    
    entities = nlp.extract_entities(text)
    complexity = nlp.analyze_complexity(text)
    sentiment = nlp.analyze_sentiment(text)
    
    return jsonify({
        'entities': entities,
        'complexity': complexity,
        'sentiment': sentiment
    })

@app.route('/api/process-document', methods=['POST'])
@handle_errors
@login_required
def process_document():
    try:
        data = request.json
        doc_path = data.get('path', '')
        
        if not doc_path:
            raise ValidationError("No document path provided")
        
        if not os.path.exists(doc_path):
            raise NotFoundError("Document", doc_path)
        
        # Check file extension
        if not (doc_path.lower().endswith('.docx') or doc_path.lower().endswith('.txt')):
            raise ValidationError("Unsupported file format. Only .docx and .txt files are supported.")
        
        # Process the document
        if doc_path.lower().endswith('.docx'):
            tasks = sprint_processor.process_document(doc_path)
        elif doc_path.lower().endswith('.txt'):
            tasks = sprint_processor.process_text_document(doc_path)
        
        if not tasks or len(tasks) == 0:
            raise ConflictError("No tasks could be extracted from the document. Please ensure the document contains properly formatted tasks.")
        
        # Create tickets from the extracted tasks
        created_tickets = []
        for task in tasks:
            ticket = system.process_feature_story(task)
            created_tickets.append(ticket)
        
        return jsonify({
            'message': 'Document processed successfully',
            'tasks_extracted': len(tasks),
            'tickets_created': len(created_tickets),
            'tickets': created_tickets
        })
    
    except Exception as e:
        app.logger.error(f"Error processing document: {str(e)}")
        app.logger.error(traceback.format_exc())
        raise ConflictError(f"Error processing document: {str(e)}")

@app.route('/api/process-sprint-document', methods=['POST'])
@handle_errors
@login_required
def process_sprint_document():
    try:
        data = request.json
        doc_path = data.get('path', '')
        
        if not doc_path:
            raise ValidationError("No document path provided")
        
        if not os.path.exists(doc_path):
            raise NotFoundError("Document", doc_path)
        
        # Check file extension
        if not (doc_path.lower().endswith('.docx') or doc_path.lower().endswith('.txt')):
            raise ValidationError("Unsupported file format. Only .docx and .txt files are supported.")
        
        # Process the sprint document
        result = sprint_processor.process_sprint_document_with_stories(doc_path)
        
        if not result:
            raise ConflictError("Failed to process sprint document. The document may not contain the required format (Sprint Goal and User Stories with Story Points).")
        
        if not result.get('tasks') or len(result['tasks']) == 0:
            raise ConflictError("No tasks could be generated from the sprint document. Please ensure the document contains properly formatted user stories.")
        
        # Create tickets from the extracted tasks
        created_tickets = []
        for task in result['tasks']:
            ticket = system.process_feature_story(task)
            created_tickets.append(ticket)
        
        return jsonify({
            'message': 'Sprint document processed successfully',
            'sprint_goal': result.get('sprint_goal', 'No sprint goal found'),
            'user_stories': result.get('user_stories', []),
            'tasks_extracted': len(result['tasks']),
            'tickets_created': len(created_tickets),
            'tickets': created_tickets
        })
    
    except Exception as e:
        app.logger.error(f"Error processing sprint document: {str(e)}")
        app.logger.error(traceback.format_exc())
        raise ConflictError(f"Error processing sprint document: {str(e)}")

@app.route('/api/tickets/<int:ticket_id>/export-jira', methods=['POST'])
@handle_errors
@login_required
def export_ticket_to_jira(ticket_id):
    success = system.export_ticket_to_jira(ticket_id)
    if success:
        return jsonify({'success': True})
    raise ConflictError("Export failed")

@app.route('/api/tickets/<int:ticket_id>/update-jira-status', methods=['POST'])
@handle_errors
@login_required
def update_jira_ticket_status(ticket_id):
    data = request.json
    status = data.get('status')
    
    if not status:
        raise ValidationError("Status is required")
    
    success = system.update_jira_ticket_status(ticket_id, status)
    if success:
        return jsonify({'success': True})
    raise ConflictError("Update failed")

@app.route('/api/system/optimize-workload', methods=['POST'])
@handle_errors
@login_required
def optimize_workload():
    assignments = system.optimize_workload()
    return jsonify({'assignments': assignments})

@app.route('/api/system/balance-workload', methods=['GET'])
@handle_errors
@login_required
def balance_workload():
    balance_info = system.balance_workload()
    return jsonify(balance_info)

@app.route('/api/system/progress-report', methods=['GET'])
@handle_errors
@login_required
def get_progress_report():
    report = system.generate_progress_report()
    return jsonify(report)

@app.route('/api/system/real-time-metrics', methods=['GET'])
@handle_errors
@login_required
def get_real_time_metrics():
    metrics = system.get_real_time_metrics()
    return jsonify(metrics)

@app.route('/api/system/adjust-priorities', methods=['POST'])
@handle_errors
@login_required
def adjust_priorities():
    adjustments = system.adjust_priorities_dynamically()
    return jsonify({'adjustments': adjustments})

@app.route('/api/dashboard', methods=['GET'])
@handle_errors
@login_required
def get_dashboard():
    generator = DashboardDataGenerator()
    dashboard_data = generator.generate_dashboard_data(
        system.tickets, 
        system.developers, 
        system.performance_tracker.get_historical_performance_data()
    )
    return jsonify(dashboard_data)

@app.route('/api/system/reset', methods=['POST'])
@handle_errors
@admin_required
def reset_system():
    # Reset system to initial state
    system.__init__()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)