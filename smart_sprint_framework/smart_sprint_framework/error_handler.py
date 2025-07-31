import traceback
import logging
from functools import wraps
from flask import jsonify
import sys
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SmartSprintException(Exception):
    """Base exception for Smart Sprint application"""
    def __init__(self, message, status_code=500, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = {
            'error': self.message,
            'status_code': self.status_code
        }
        if self.payload:
            rv.update(self.payload)
        return rv

class ValidationError(SmartSprintException):
    """Exception for validation errors"""
    def __init__(self, message, field=None):
        super().__init__(message, status_code=400)
        self.field = field

class AuthenticationError(SmartSprintException):
    """Exception for authentication errors"""
    def __init__(self, message):
        super().__init__(message, status_code=401)

class AuthorizationError(SmartSprintException):
    """Exception for authorization errors"""
    def __init__(self, message):
        super().__init__(message, status_code=403)

class NotFoundError(SmartSprintException):
    """Exception for not found errors"""
    def __init__(self, resource, resource_id=None):
        message = f"{resource} not found"
        if resource_id:
            message += f": {resource_id}"
        super().__init__(message, status_code=404)

class ConflictError(SmartSprintException):
    """Exception for conflict errors"""
    def __init__(self, message):
        super().__init__(message, status_code=409)

def handle_errors(f):
    """Decorator to handle exceptions in Flask routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SmartSprintException as e:
            logger.error(f"SmartSprintException: {str(e)}")
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Create error report
            error_report = create_error_report(e)
            
            response = jsonify({
                'error': 'An unexpected error occurred',
                'error_id': error_report['error_id'],
                'status_code': 500
            })
            response.status_code = 500
            return response
    
    return decorated_function

def create_error_report(exception):
    """Create a detailed error report"""
    error_id = f"ERR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    error_report = {
        'error_id': error_id,
        'timestamp': datetime.now().isoformat(),
        'exception_type': type(exception).__name__,
        'exception_message': str(exception),
        'traceback': traceback.format_exc(),
        'python_version': sys.version,
        'platform': sys.platform
    }
    
    # Save error report to file
    os.makedirs('error_reports', exist_ok=True)
    report_path = f"error_reports/{error_id}.json"
    
    try:
        import json
        with open(report_path, 'w') as f:
            json.dump(error_report, f, indent=2)
        logger.info(f"Error report saved to {report_path}")
    except Exception as e:
        logger.error(f"Failed to save error report: {str(e)}")
    
    return error_report

def safe_execute(func, default_return=None, log_errors=True):
    """Safely execute a function with error handling"""
    try:
        return func()
    except Exception as e:
        if log_errors:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
        return default_return

def retry_operation(func, max_attempts=3, delay=1, backoff=2, exceptions=None):
    """Retry an operation with exponential backoff"""
    if exceptions is None:
        exceptions = (Exception,)
    
    attempt = 0
    current_delay = delay
    
    while attempt < max_attempts:
        try:
            return func()
        except exceptions as e:
            attempt += 1
            if attempt >= max_attempts:
                logger.error(f"Operation failed after {max_attempts} attempts: {str(e)}")
                raise
            
            logger.warning(f"Operation failed (attempt {attempt}/{max_attempts}): {str(e)}. Retrying in {current_delay}s...")
            import time
            time.sleep(current_delay)
            current_delay *= backoff
    
    return None

def validate_required_fields(data, required_fields):
    """Validate that required fields are present in data"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing_fields.append(field)
    
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

def validate_field_types(data, field_types):
    """Validate that fields have the correct types"""
    type_errors = []
    
    for field, expected_type in field_types.items():
        if field in data and not isinstance(data[field], expected_type):
            type_errors.append(f"Field '{field}' must be of type {expected_type.__name__}")
    
    if type_errors:
        raise ValidationError("; ".join(type_errors))

def validate_positive_numbers(data, fields):
    """Validate that specified fields are positive numbers"""
    number_errors = []
    
    for field in fields:
        if field in data:
            try:
                value = float(data[field])
                if value <= 0:
                    number_errors.append(f"Field '{field}' must be a positive number")
            except (ValueError, TypeError):
                number_errors.append(f"Field '{field}' must be a number")
    
    if number_errors:
        raise ValidationError("; ".join(number_errors))