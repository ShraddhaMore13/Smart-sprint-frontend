import sqlite3
import json
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='smart_sprint.db'):
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create developers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS developers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            skills TEXT,  -- JSON array
            availability INTEGER,
            current_workload REAL,
            experience_level INTEGER
        )
        ''')
        
        # Create tickets table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            complexity INTEGER,
            estimated_hours REAL,
            status TEXT,
            tasks TEXT,  -- JSON array
            assigned_to INTEGER,
            entities TEXT,  -- JSON object
            dependencies TEXT,  -- JSON array
            deadline TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES developers(id)
        )
        ''')
        
        # Create performance_metrics table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            developer_id INTEGER,
            ticket_id INTEGER,
            completion_time REAL,
            revisions INTEGER,
            sentiment_score REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (developer_id) REFERENCES developers(id),
            FOREIGN KEY (ticket_id) REFERENCES tickets(id)
        )
        ''')
        
        # Create comments table for sentiment analysis
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER,
            developer_id INTEGER,
            comment TEXT,
            sentiment_label TEXT,
            sentiment_score REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id),
            FOREIGN KEY (developer_id) REFERENCES developers(id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)
    
    # Developer operations
    def add_developer(self, developer):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO developers (name, skills, availability, current_workload, experience_level)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            developer['name'],
            json.dumps(developer['skills']),
            developer['availability'],
            developer['current_workload'],
            developer.get('experience_level', 3)
        ))
        
        developer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return developer_id
    
    def get_developers(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM developers')
        developers = []
        
        for row in cursor.fetchall():
            developer = dict(row)
            developer['skills'] = json.loads(developer['skills'])
            developers.append(developer)
        
        conn.close()
        return developers
    
    def update_developer(self, developer_id, updates):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        values = []
        
        for field, value in updates.items():
            if field == 'skills':
                update_fields.append(f"{field} = ?")
                values.append(json.dumps(value))
            else:
                update_fields.append(f"{field} = ?")
                values.append(value)
        
        if update_fields:
            query = f"UPDATE developers SET {', '.join(update_fields)} WHERE id = ?"
            values.append(developer_id)
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
    
    # Ticket operations
    def add_ticket(self, ticket):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO tickets (title, description, priority, complexity, estimated_hours, status, tasks, assigned_to, entities, dependencies, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ticket['title'],
            ticket['description'],
            ticket['priority'],
            ticket['complexity'],
            ticket['estimated_hours'],
            ticket['status'],
            json.dumps(ticket.get('tasks', [])),
            ticket.get('assigned_to'),
            json.dumps(ticket.get('entities', {})),
            json.dumps(ticket.get('dependencies', [])),
            ticket.get('deadline')
        ))
        
        ticket_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return ticket_id
    
    def get_tickets(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tickets ORDER BY created_at DESC')
        tickets = []
        
        for row in cursor.fetchall():
            ticket = dict(row)
            ticket['tasks'] = json.loads(ticket['tasks'])
            ticket['entities'] = json.loads(ticket['entities'])
            ticket['dependencies'] = json.loads(ticket['dependencies'])
            tickets.append(ticket)
        
        conn.close()
        return tickets
    
    def update_ticket(self, ticket_id, updates):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        values = []
        
        for field, value in updates.items():
            if field in ['tasks', 'entities', 'dependencies']:
                update_fields.append(f"{field} = ?")
                values.append(json.dumps(value))
            else:
                update_fields.append(f"{field} = ?")
                values.append(value)
        
        if update_fields:
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE tickets SET {', '.join(update_fields)} WHERE id = ?"
            values.append(ticket_id)
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
    
    # Performance metrics operations
    def add_performance_metric(self, metric):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO performance_metrics (developer_id, ticket_id, completion_time, revisions, sentiment_score)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            metric['developer_id'],
            metric['ticket_id'],
            metric['completion_time'],
            metric['revisions'],
            metric['sentiment_score']
        ))
        
        metric_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return metric_id
    
    def get_performance_metrics(self, developer_id=None):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if developer_id:
            cursor.execute('SELECT * FROM performance_metrics WHERE developer_id = ? ORDER BY timestamp DESC', (developer_id,))
        else:
            cursor.execute('SELECT * FROM performance_metrics ORDER BY timestamp DESC')
        
        metrics = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return metrics
    
    # Comments operations for sentiment analysis
    def add_comment(self, comment):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO comments (ticket_id, developer_id, comment, sentiment_label, sentiment_score)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            comment['ticket_id'],
            comment['developer_id'],
            comment['comment'],
            comment.get('sentiment_label'),
            comment.get('sentiment_score')
        ))
        
        comment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return comment_id
    
    def get_comments(self, ticket_id=None):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if ticket_id:
            cursor.execute('SELECT * FROM comments WHERE ticket_id = ? ORDER BY timestamp DESC', (ticket_id,))
        else:
            cursor.execute('SELECT * FROM comments ORDER BY timestamp DESC')
        
        comments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return comments
    
    # Utility methods
    def backup_database(self, backup_path=None):
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backups/smart_sprint_{timestamp}.db"
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Create backup
        import shutil
        shutil.copy2(self.db_path, backup_path)
        return backup_path