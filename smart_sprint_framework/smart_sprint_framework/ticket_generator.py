import json
from nlp_pipeline import NLPPipeline

class TicketGenerator:
    def __init__(self, nlp_pipeline):
        self.nlp = nlp_pipeline
    
    def generate_ticket(self, feature_story):
        entities = self.nlp.extract_entities(feature_story['description'])
        complexity = self.nlp.analyze_complexity(feature_story['description'])
        
        # Generate tasks based on the ticket title
        tasks = self._generate_tasks(feature_story['title'], complexity)
        
        ticket = {
            'id': None,
            'title': feature_story['title'],
            'description': feature_story['description'],
            'priority': feature_story['priority'],
            'complexity': complexity,
            'estimated_hours': feature_story['estimated_hours'],
            'status': 'backlog',
            'tasks': tasks,
            'entities': entities
        }
        
        return ticket
    
    def _generate_tasks(self, title, complexity):
        title_lower = title.lower()
        
        # Define specific tasks based on ticket title
        if 'security audit' in title_lower:
            return [
                "Review application architecture for security vulnerabilities",
                "Conduct penetration testing",
                "Implement security fixes",
                "Update security documentation",
                "Verify security compliance"
            ]
        elif 'logging' in title_lower and 'error' in title_lower:
            return [
                "Design logging architecture",
                "Implement error tracking system",
                "Create log aggregation pipeline",
                "Set up alerting for critical errors",
                "Develop log analysis dashboard"
            ]
        elif 'database schema' in title_lower:
            return [
                "Analyze data requirements",
                "Design database schema",
                "Implement database migrations",
                "Create database indexes",
                "Test database performance"
            ]
        elif 'authentication' in title_lower:
            return [
                "Design authentication flow",
                "Implement OAuth2 integration",
                "Create session management",
                "Develop password reset functionality",
                "Test authentication security"
            ]
        elif 'api endpoints' in title_lower:
            return [
                "Design API specification",
                "Implement REST endpoints",
                "Create API documentation",
                "Add request validation",
                "Test API functionality"
            ]
        elif 'dashboard' in title_lower:
            return [
                "Design dashboard layout",
                "Implement data visualization",
                "Create dashboard filters",
                "Add real-time updates",
                "Test dashboard performance"
            ]
        elif 'payment gateway' in title_lower:
            return [
                "Research payment gateway options",
                "Implement payment processing",
                "Create transaction history",
                "Add refund functionality",
                "Test payment security"
            ]
        elif 'email notification' in title_lower:
            return [
                "Design email templates",
                "Implement email sending",
                "Create email queue system",
                "Add email tracking",
                "Test email delivery"
            ]
        elif 'file upload' in title_lower:
            return [
                "Design file upload interface",
                "Implement file storage",
                "Add file validation",
                "Create file preview",
                "Test upload performance"
            ]
        elif 'search functionality' in title_lower:
            return [
                "Design search architecture",
                "Implement search indexing",
                "Create search filters",
                "Add search suggestions",
                "Test search relevance"
            ]
        elif 'user profile' in title_lower:
            return [
                "Design profile page",
                "Implement profile updates",
                "Add profile picture upload",
                "Create privacy settings",
                "Test profile functionality"
            ]
        elif 'access control' in title_lower:
            return [
                "Design permission system",
                "Implement role management",
                "Create access control UI",
                "Add permission inheritance",
                "Test access security"
            ]
        elif 'real-time chat' in title_lower:
            return [
                "Design chat architecture",
                "Implement WebSocket connection",
                "Create message storage",
                "Add chat notifications",
                "Test chat performance"
            ]
        elif 'data export' in title_lower:
            return [
                "Design export formats",
                "Implement CSV export",
                "Create PDF export",
                "Add export scheduling",
                "Test export functionality"
            ]
        elif 'responsive design' in title_lower:
            return [
                "Analyze current design",
                "Implement responsive layout",
                "Test on mobile devices",
                "Optimize images for mobile",
                "Test cross-browser compatibility"
            ]
        # Add specific tasks for password reset functionality
        elif 'password reset' in title_lower:
            return [
                "Design password reset flow",
                "Implement password reset request form",
                "Create secure token generation",
                "Implement email notification system",
                "Develop password update page",
                "Test password reset functionality"
            ]
        elif 'email sending' in title_lower:
            return [
                "Design email template",
                "Implement email service integration",
                "Create email queue system",
                "Add email tracking",
                "Test email delivery"
            ]
        elif 'password reset page' in title_lower:
            return [
                "Design password reset page layout",
                "Implement secure token validation",
                "Create password update form",
                "Add password strength validation",
                "Test page functionality"
            ]
        elif 'password update' in title_lower:
            return [
                "Design password update logic",
                "Implement password hashing",
                "Create password validation",
                "Update user authentication",
                "Test password update functionality"
            ]
        elif 'confirmation page' in title_lower:
            return [
                "Design confirmation page layout",
                "Implement success message display",
                "Add redirect to login",
                "Create user notification",
                "Test confirmation flow"
            ]
        elif 'test password reset' in title_lower:
            return [
                "Create test plan for password reset",
                "Test password reset request",
                "Test email notification",
                "Test password update",
                "Test security aspects",
                "Document test results"
            ]
        # Add more specific ticket types as needed
        elif 'user registration' in title_lower:
            return [
                "Design registration form",
                "Implement user registration logic",
                "Create email verification system",
                "Develop registration confirmation page",
                "Test registration process"
            ]
        elif 'login form' in title_lower:
            return [
                "Design login form layout",
                "Implement authentication logic",
                "Add remember me functionality",
                "Create forgot password link",
                "Test login functionality"
            ]
        elif 'user management' in title_lower:
            return [
                "Design user management interface",
                "Implement CRUD operations for users",
                "Create user search and filtering",
                "Add role assignment functionality",
                "Test user management features"
            ]
        elif 'role management' in title_lower:
            return [
                "Design role management system",
                "Implement role creation and editing",
                "Create permission assignment interface",
                "Add role inheritance support",
                "Test role management functionality"
            ]
        elif 'permission system' in title_lower:
            return [
                "Design permission architecture",
                "Implement permission checking logic",
                "Create permission management interface",
                "Add permission inheritance",
                "Test permission system"
            ]
        elif 'session management' in title_lower:
            return [
                "Design session management architecture",
                "Implement session creation and validation",
                "Create session timeout handling",
                "Add session security features",
                "Test session management"
            ]
        elif 'token authentication' in title_lower:
            return [
                "Design token-based authentication",
                "Implement JWT token generation",
                "Create token validation logic",
                "Add token refresh functionality",
                "Test token authentication"
            ]
        elif 'oauth integration' in title_lower:
            return [
                "Design OAuth integration architecture",
                "Implement OAuth provider connections",
                "Create user authentication flow",
                "Add token management",
                "Test OAuth integration"
            ]
        elif 'two factor authentication' in title_lower or '2fa' in title_lower:
            return [
                "Design 2FA implementation",
                "Implement SMS/Email verification",
                "Create authenticator app integration",
                "Add backup code functionality",
                "Test 2FA implementation"
            ]
        elif 'data validation' in title_lower:
            return [
                "Design validation rules",
                "Implement client-side validation",
                "Create server-side validation",
                "Add validation error handling",
                "Test validation functionality"
            ]
        elif 'form validation' in title_lower:
            return [
                "Design form validation strategy",
                "Implement input validation",
                "Create validation error messages",
                "Add real-time validation feedback",
                "Test form validation"
            ]
        elif 'input sanitization' in title_lower:
            return [
                "Design input sanitization strategy",
                "Implement sanitization filters",
                "Create XSS prevention measures",
                "Add SQL injection protection",
                "Test input sanitization"
            ]
        elif 'security headers' in title_lower:
            return [
                "Design security headers implementation",
                "Implement CSP headers",
                "Create security middleware",
                "Add security header testing",
                "Test security headers"
            ]
        elif 'cors configuration' in title_lower:
            return [
                "Design CORS policy",
                "Implement CORS middleware",
                "Create CORS configuration for different environments",
                "Add CORS error handling",
                "Test CORS configuration"
            ]
        elif 'rate limiting' in title_lower:
            return [
                "Design rate limiting strategy",
                "Implement rate limiting middleware",
                "Create rate limit configuration",
                "Add rate limit exceeded handling",
                "Test rate limiting"
            ]
        elif 'caching strategy' in title_lower:
            return [
                "Design caching architecture",
                "Implement caching layer",
                "Create cache invalidation strategy",
                "Add cache monitoring",
                "Test caching implementation"
            ]
        elif 'performance optimization' in title_lower:
            return [
                "Analyze performance bottlenecks",
                "Implement performance optimizations",
                "Create performance monitoring",
                "Add load testing",
                "Test performance improvements"
            ]
        elif 'load testing' in title_lower:
            return [
                "Design load testing strategy",
                "Implement load testing scripts",
                "Create performance benchmarks",
                "Analyze load testing results",
                "Document performance findings"
            ]
        elif 'monitoring system' in title_lower:
            return [
                "Design monitoring architecture",
                "Implement monitoring agents",
                "Create monitoring dashboards",
                "Add alerting system",
                "Test monitoring functionality"
            ]
        elif 'alerting system' in title_lower:
            return [
                "Design alerting rules",
                "Implement alert notification system",
                "Create alert management interface",
                "Add alert escalation rules",
                "Test alerting system"
            ]
        elif 'logging system' in title_lower:
            return [
                "Design logging architecture",
                "Implement structured logging",
                "Create log aggregation",
                "Add log search functionality",
                "Test logging system"
            ]
        elif 'error tracking' in title_lower:
            return [
                "Design error tracking system",
                "Implement error capture",
                "Create error reporting",
                "Add error analysis tools",
                "Test error tracking"
            ]
        elif 'documentation' in title_lower:
            return [
                "Design documentation structure",
                "Implement API documentation",
                "Create user guides",
                "Add code documentation",
                "Test documentation completeness"
            ]
        elif 'unit testing' in title_lower:
            return [
                "Design unit testing strategy",
                "Implement unit tests",
                "Create test coverage reports",
                "Add continuous integration testing",
                "Test test framework"
            ]
        elif 'integration testing' in title_lower:
            return [
                "Design integration testing strategy",
                "Implement integration tests",
                "Create test environment setup",
                "Add test data management",
                "Test integration scenarios"
            ]
        elif 'e2e testing' in title_lower or 'end to end testing' in title_lower:
            return [
                "Design E2E testing strategy",
                "Implement E2E test scenarios",
                "Create test automation scripts",
                "Add cross-browser testing",
                "Test E2E workflows"
            ]
        elif 'deployment pipeline' in title_lower:
            return [
                "Design deployment architecture",
                "Implement CI/CD pipeline",
                "Create deployment scripts",
                "Add environment management",
                "Test deployment process"
            ]
        elif 'docker containerization' in title_lower:
            return [
                "Design Docker architecture",
                "Implement Dockerfile creation",
                "Create docker-compose configuration",
                "Add container orchestration",
                "Test container deployment"
            ]
        elif 'kubernetes deployment' in title_lower:
            return [
                "Design Kubernetes architecture",
                "Implement Kubernetes manifests",
                "Create deployment configurations",
                "Add service discovery",
                "Test Kubernetes deployment"
            ]
        elif 'cloud migration' in title_lower:
            return [
                "Design cloud migration strategy",
                "Implement cloud infrastructure",
                "Create migration scripts",
                "Add data migration plan",
                "Test cloud deployment"
            ]
        elif 'backup system' in title_lower:
            return [
                "Design backup strategy",
                "Implement backup automation",
                "Create backup verification",
                "Add disaster recovery plan",
                "Test backup and restore"
            ]
        elif 'disaster recovery' in title_lower:
            return [
                "Design disaster recovery plan",
                "Implement recovery procedures",
                "Create recovery testing",
                "Add recovery documentation",
                "Test disaster recovery"
            ]
        else:
            # Default tasks based on complexity
            task_templates = {
                1: ["Analyze requirements", "Create basic implementation"],
                2: ["Design solution", "Implement core functionality", "Create basic tests"],
                3: ["Design architecture", "Implement core features", "Create unit tests", "Document API"],
                4: ["Design system architecture", "Implement core features", "Create comprehensive tests", 
                    "Document API endpoints", "Set up monitoring"],
                5: ["Design scalable architecture", "Implement core features", "Create comprehensive tests",
                    "Document API endpoints", "Set up monitoring", "Performance optimization", 
                    "Security review"]
            }
            return task_templates.get(complexity, ["Analyze requirements", "Implement solution"])