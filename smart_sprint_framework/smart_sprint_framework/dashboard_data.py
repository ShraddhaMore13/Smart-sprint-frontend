import datetime
import numpy as np
from collections import defaultdict, Counter
import ast  # For parsing string representations of lists

class DashboardDataGenerator:
    def __init__(self):
        pass
    
    def generate_dashboard_data(self, tickets, developers, performance_data):
        """Generate comprehensive data for dashboard visualization"""
        dashboard_data = {
            'summary': self._generate_summary_data(tickets, developers),
            'ticket_trends': self._generate_ticket_trends(tickets),
            'developer_performance': self._generate_developer_performance_data(developers, performance_data),
            'priority_distribution': self._generate_priority_distribution(tickets),
            'complexity_analysis': self._generate_complexity_analysis(tickets),
            'workload_distribution': self._generate_workload_distribution(developers),
            'velocity_tracking': self._generate_velocity_tracking(tickets, performance_data),
            'burndown_data': self._generate_burndown_data(tickets)
        }
        
        return dashboard_data
    
    def _generate_summary_data(self, tickets, developers):
        """Generate summary statistics"""
        total_tickets = len(tickets)
        completed_tickets = len([t for t in tickets if t['status'] == 'completed'])
        in_progress_tickets = len([t for t in tickets if t['status'] == 'in_progress'])
        backlog_tickets = len([t for t in tickets if t['status'] == 'backlog'])
        
        total_workload = sum(dev['current_workload'] for dev in developers)
        total_availability = sum(dev['availability'] for dev in developers)
        utilization_rate = (total_workload / total_availability * 100) if total_availability > 0 else 0
        
        # Calculate completion rate
        completion_rate = (completed_tickets / total_tickets * 100) if total_tickets > 0 else 0
        
        # Calculate average completion time
        completed_with_time = [t for t in tickets if t['status'] == 'completed' and t.get('completion_time')]
        avg_completion_time = np.mean([t['completion_time'] for t in completed_with_time]) if completed_with_time else 0
        
        return {
            'total_tickets': total_tickets,
            'completed_tickets': completed_tickets,
            'in_progress_tickets': in_progress_tickets,
            'backlog_tickets': backlog_tickets,
            'completion_rate': round(completion_rate, 1),
            'utilization_rate': round(utilization_rate, 1),
            'avg_completion_time': round(avg_completion_time, 1)
        }
    
    def _generate_ticket_trends(self, tickets):
        """Generate ticket trend data over time"""
        # For this example, we'll generate mock trend data
        # In a real system, you would track creation and completion dates
        
        days = 14
        trend_data = []
        
        for i in range(days):
            date = datetime.datetime.now() - datetime.timedelta(days=days-i-1)
            
            # Generate mock data
            created = np.random.randint(0, 5)
            completed = np.random.randint(0, 3)
            
            trend_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'created': created,
                'completed': completed,
                'backlog_change': created - completed
            })
        
        return trend_data
    
    def _generate_developer_performance_data(self, developers, performance_data):
        """Generate developer performance metrics"""
        performance_metrics = []
        
        for dev in developers:
            dev_id = dev['id']
            perf_data = performance_data.get(dev_id, {})
            
            # Calculate metrics
            utilization = (dev['current_workload'] / dev['availability'] * 100) if dev['availability'] > 0 else 0
            
            # Get performance metrics
            velocity = perf_data.get('velocity', 0)
            accuracy = perf_data.get('accuracy', 0)
            sentiment = perf_data.get('sentiment', 0)
            tickets_completed = perf_data.get('tickets_completed', 0)
            
            # If we don't have performance data, generate some sample data
            if velocity == 0 and tickets_completed == 0:
                # Generate sample data for demonstration
                velocity = np.random.uniform(8, 20)
                accuracy = np.random.uniform(0.7, 0.95)
                sentiment = np.random.uniform(0.6, 0.9)
                tickets_completed = np.random.randint(3, 8)
            
            # Ensure skills are always a list
            skills = dev['skills']
            if isinstance(skills, str):
                try:
                    skills = ast.literal_eval(skills)
                except (ValueError, SyntaxError):
                    # If that fails, try splitting by comma
                    skills = [skill.strip() for skill in skills.split(',')]
            
            performance_metrics.append({
                'developer_id': dev_id,
                'developer_name': dev['name'],
                'utilization': round(utilization, 1),
                'velocity': round(velocity, 1),
                'accuracy': round(accuracy * 100, 1),  # Convert to percentage
                'sentiment': round(sentiment * 100, 1),  # Convert to percentage
                'tickets_completed': tickets_completed,
                'availability': dev['availability'],
                'current_workload': dev['current_workload'],
                'skills': skills  # Ensure skills is a list
            })
        
        return performance_metrics
    
    def _generate_priority_distribution(self, tickets):
        """Generate priority distribution data"""
        priority_counts = Counter(ticket['priority'] for ticket in tickets)
        
        total = sum(priority_counts.values())
        
        distribution = []
        for priority, count in priority_counts.items():
            distribution.append({
                'priority': priority,
                'count': count,
                'percentage': round((count / total * 100), 1) if total > 0 else 0
            })
        
        return distribution
    
    def _generate_complexity_analysis(self, tickets):
        """Generate complexity analysis data"""
        complexity_counts = Counter(ticket['complexity'] for ticket in tickets)
        
        total = sum(complexity_counts.values())
        
        analysis = []
        for complexity in range(1, 6):  # Complexity levels 1-5
            count = complexity_counts.get(complexity, 0)
            analysis.append({
                'complexity': complexity,
                'count': count,
                'percentage': round((count / total * 100), 1) if total > 0 else 0
            })
        
        return analysis
    
    def _generate_workload_distribution(self, developers):
        """Generate workload distribution data"""
        workload_data = []
        
        for dev in developers:
            workload_data.append({
                'developer_id': dev['id'],
                'developer_name': dev['name'],
                'current_workload': dev['current_workload'],
                'availability': dev['availability'],
                'remaining_capacity': dev['availability'] - dev['current_workload'],
                'utilization': round((dev['current_workload'] / dev['availability'] * 100), 1) if dev['availability'] > 0 else 0
            })
        
        return workload_data
    
    def _generate_velocity_tracking(self, tickets, performance_data):
        """Generate velocity tracking data"""
        # For this example, we'll generate mock velocity data
        # In a real system, you would track velocity over time
        
        weeks = 8
        velocity_data = []
        
        # Calculate average velocity from performance data
        all_velocity = [perf.get('velocity', 0) for perf in performance_data.values() if perf.get('velocity', 0) > 0]
        avg_velocity = np.mean(all_velocity) if all_velocity else 15  # Default if no data
        
        for i in range(weeks):
            week_start = datetime.datetime.now() - datetime.timedelta(weeks=weeks-i)
            week_end = week_start + datetime.timedelta(days=7)
            
            # Generate mock velocity data with some variation
            variation = np.random.uniform(0.8, 1.2)
            planned_velocity = round(avg_velocity * variation)
            actual_velocity = round(planned_velocity * np.random.uniform(0.7, 1.1))
            
            velocity_data.append({
                'week': f"Week {i+1}",
                'week_start': week_start.strftime('%Y-%m-%d'),
                'planned_velocity': planned_velocity,
                'actual_velocity': actual_velocity,
                'variance': actual_velocity - planned_velocity,
                'variance_percentage': round(((actual_velocity - planned_velocity) / planned_velocity * 100), 1) if planned_velocity > 0 else 0
            })
        
        return velocity_data
    
    def _generate_burndown_data(self, tickets):
        """Generate burndown chart data"""
        # For this example, we'll generate mock burndown data
        # In a real system, you would track remaining work over time
        
        days = 14
        total_work = sum(ticket['estimated_hours'] for ticket in tickets if ticket['status'] != 'completed')
        
        burndown_data = []
        remaining_work = total_work
        
        for i in range(days):
            date = datetime.datetime.now() - datetime.timedelta(days=days-i-1)
            
            # Generate mock burndown data
            if remaining_work > 0:
                # More work gets done in the middle of the sprint
                if i < days * 0.3:
                    progress_factor = 0.05
                elif i < days * 0.7:
                    progress_factor = 0.1
                else:
                    progress_factor = 0.15
                
                completed_today = min(remaining_work * progress_factor, remaining_work)
                remaining_work -= completed_today
            else:
                completed_today = 0
            
            burndown_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'remaining_work': round(remaining_work, 1),
                'ideal_remaining': round(total_work * (1 - i/days), 1),
                'completed_today': completed_today
            })
        
        return burndown_data