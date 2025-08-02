import jwt
import functools
from datetime import datetime, timedelta
from flask import request, jsonify, current_app

# User database with plaintext passwords for testing
users = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "user": {
        "password": "user123",
        "role": "user"
    }
}

def verify_password(username, password):
    """Verify if the provided password matches the stored password for the given username."""
    if username not in users:
        print(f"DEBUG: User {username} not found")
        return False
    
    stored_password = users[username]["password"]
    
    print(f"DEBUG: Username: {username}")
    print(f"DEBUG: Provided password: {password}")
    print(f"DEBUG: Stored password: {stored_password}")
    print(f"DEBUG: Passwords match: {stored_password == password}")
    
    # Compare the passwords directly (plaintext for now)
    return stored_password == password

def generate_token(username):
    """Generate a JWT token for the authenticated user."""
    payload = {
        'username': username,
        'role': users[username]["role"],
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }
    
    # Use a fixed secret key instead of trying to get it from app config
    secret_key = 'your_secure_secret_key_here'
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def login_required(f):
    """Decorator to require authentication for a route."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Authorization token is required'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
                
            # Use the same fixed secret key
            secret_key = 'your_secure_secret_key_here'
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            request.current_user = payload['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for a route."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Authorization token is required'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
                
            # Use the same fixed secret key
            secret_key = 'your_secure_secret_key_here'
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            if payload.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
                
            request.current_user = payload['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    return decorated_function