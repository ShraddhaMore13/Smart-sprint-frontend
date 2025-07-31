import hashlib
import jwt
import datetime
from functools import wraps
from flask import request, jsonify

# Secret key for JWT
SECRET_KEY = "smart_sprint_secret_key"

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

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(username, password):
    """Verify user password"""
    if username in users:
        return users[username]["password"] == hash_password(password)
    return False

def generate_token(username):
    """Generate JWT token"""
    payload = {
        "username": username,
        "role": users[username]["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        try:
            # Remove "Bearer " prefix if present
            if token.startswith("Bearer "):
                token = token[7:]
            
            payload = verify_token(token)
            if not payload:
                return jsonify({"error": "Token is invalid"}), 401
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        try:
            # Remove "Bearer " prefix if present
            if token.startswith("Bearer "):
                token = token[7:]
            
            payload = verify_token(token)
            if not payload:
                return jsonify({"error": "Token is invalid"}), 401
            
            if payload.get("role") != "admin":
                return jsonify({"error": "Admin access required"}), 403
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401
    
    return decorated