import datetime
from collections import defaultdict
import numpy as np

class ProgressMonitor:
    def __init__(self):
        self.bottleneck_threshold = 0.8  # 80% utilization considered bottleneck
        self.slow_task_threshold = 1.5  # 50% over estimated time considered slow
    
    def generate_progress_report(self, tickets, developers, performance_data):
        """Generate a comprehensive progress report"""
        # Calculate overall metrics
        total_tickets = len(tickets)
        completed_tickets = len([t for t in tickets if t['status'] == 'completed'])
        in_progress_tickets = len([t for t in tickets if t['status'] == 'in_progress'])
        backlog_tickets = len([t for t in tickets if t['status'] == 'backlog'])
        
        completion_rate = completed_tickets / total_tickets if total_tickets > 0 else 0
        
        # Calculate developer metrics
        developer_metrics = []
        for dev in developers:
            dev_tickets = [t for t in tickets if t.get('assigned_to') == dev['id']]
            completed_dev_tickets = [t for t in dev_tickets if t['status'] == 'completed']
            
            utilization = dev['current_workload'] / dev['availability'] if dev['availability'] > 0 else 0
            
            # Get performance data
            perf_data = performance_data.get(dev['id'], {})
            avg_completion_time = perf_data.get('velocity', 0)
            accuracy = perf_data.get('accuracy', 0)
            
            developer_metrics.append({
                'developer_id': dev['id'],
                'developer_name': dev['name'],
                'total_tickets': len(dev_tickets),
                'completed_tickets': len(completed_dev_tickets),
                'utilization': utilization,
                'avg_completion_time': avg_completion_time,
                'accuracy': accuracy
            })
        
        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(developers, tickets)
        
        # Identify slow tasks
        slow_tasks = self._identify_slow_tasks(tickets)
        
        # Generate insights
        insights = self._generate_insights(tickets, developers, bottlenecks, slow_tasks)
        
        return {
            'summary': {
                'total_tickets': total_tickets,
                'completed_tickets': completed_tickets,
                'in_progress_tickets': in_progress_tickets,
                'backlog_tickets': backlog_tickets,
                'completion_rate': completion_rate
            },
            'developer_metrics': developer_metrics,
            'bottlenecks': bottlenecks,
            'slow_tasks': slow_tasks,
            'insights': insights,
            'generated_at': datetime.datetime.now().isoformat()
        }
    
    def _identify_bottlenecks(self, developers, tickets):
        """Identify bottleneck developers and tasks"""
        bottlenecks = []
        
        # Identify overutilized developers
        for dev in developers:
            utilization = dev['current_workload'] / dev['availability'] if dev['availability'] > 0 else 0
            
            if utilization >= self.bottleneck_threshold:
                # Get tickets assigned to this developer
                dev_tickets = [t for t in tickets if t.get('assigned_to') == dev['id'] and t['status'] == 'in_progress']
                
                bottlenecks.append({
                    'type': 'developer',
                    'developer_id': dev['id'],
                    'developer_name': dev['name'],
                    'utilization': utilization,
                    'current_workload': dev['current_workload'],
                    'availability': dev['availability'],
                    'affected_tickets': len(dev_tickets),
                    'severity': 'high' if utilization > 0.9 else 'medium'
                })
        
        # Identify tasks with many dependencies
        for ticket in tickets:
            if ticket['status'] == 'backlog':
                # Count how many tasks depend on this one
                dependencies = 0
                for other_ticket in tickets:
                    if ticket['id'] in other_ticket.get('dependencies', []):
                        dependencies += 1
                
                if dependencies >= 3:  # If 3 or more tasks depend on this one
                    bottlenecks.append({
                        'type': 'task',
                        'ticket_id': ticket['id'],
                        'ticket_title': ticket['title'],
                        'dependencies': dependencies,
                        'severity': 'medium'
                    })
        
        return bottlenecks
    
    def _identify_slow_tasks(self, tickets):
        """Identify tasks that are taking longer than estimated"""
        slow_tasks = []
        
        for ticket in tickets:
            if ticket['status'] == 'in_progress' and ticket.get('assigned_to'):
                # Calculate how long the task has been in progress
                # For this example, we'll use a simplified approach
                # In a real system, you would track when the task was moved to in_progress
                
                # Check if completion time is much higher than estimated
                if ticket.get('completion_time', 0) > ticket['estimated_hours'] * self.slow_task_threshold:
                    slow_tasks.append({
                        'ticket_id': ticket['id'],
                        'ticket_title': ticket['title'],
                        'estimated_hours': ticket['estimated_hours'],
                        'actual_hours': ticket.get('completion_time', 0),
                        'overrun_ratio': ticket.get('completion_time', 0) / ticket['estimated_hours'],
                        'assigned_to': ticket.get('assigned_to')
                    })
        
        return slow_tasks
    
    def _generate_insights(self, tickets, developers, bottlenecks, slow_tasks):
        """Generate actionable insights based on the data"""
        insights = []
        
        # Overall progress insights
        total_tickets = len(tickets)
        completed_tickets = len([t for t in tickets if t['status'] == 'completed'])
        completion_rate = completed_tickets / total_tickets if total_tickets > 0 else 0
        
        if completion_rate < 0.3:
            insights.append({
                'type': 'warning',
                'message': 'Low completion rate. Consider reducing scope or adding resources.'
            })
        elif completion_rate > 0.8:
            insights.append({
                'type': 'success',
                'message': 'High completion rate. Team is performing well.'
            })
        
        # Bottleneck insights
        if bottlenecks:
            dev_bottlenecks = [b for b in bottlenecks if b['type'] == 'developer']
            if dev_bottlenecks:
                insights.append({
                    'type': 'warning',
                    'message': f'{len(dev_bottlenecks)} developer(s) are overutilized. Consider redistributing tasks.'
                })
        
        # Slow tasks insights
        if slow_tasks:
            insights.append({
                'type': 'warning',
                'message': f'{len(slow_tasks)} task(s) are taking longer than estimated. Review estimates and complexity.'
            })
        
        # Workload distribution insights
        utilizations = [dev['current_workload'] / dev['availability'] for dev in developers if dev['availability'] > 0]
        if utilizations:
            avg_utilization = np.mean(utilizations)
            max_utilization = np.max(utilizations)
            min_utilization = np.min(utilizations)
            
            if max_utilization - min_utilization > 0.5:
                insights.append({
                    'type': 'warning',
                    'message': 'Uneven workload distribution. Consider balancing tasks among developers.'
                })
        
        return insights
    
    def get_real_time_metrics(self, tickets, developers):
        """Get real-time metrics for dashboard"""
        # Calculate current metrics
        total_tickets = len(tickets)
        completed_tickets = len([t for t in tickets if t['status'] == 'completed'])
        in_progress_tickets = len([t for t in tickets if t['status'] == 'in_progress'])
        backlog_tickets = len([t for t in tickets if t['status'] == 'backlog'])
        
        # Calculate workload metrics
        total_workload = sum(dev['current_workload'] for dev in developers)
        total_availability = sum(dev['availability'] for dev in developers)
        utilization_rate = total_workload / total_availability if total_availability > 0 else 0
        
        # Calculate velocity metrics
        completed_tickets_with_time = [t for t in tickets if t['status'] == 'completed' and t.get('completion_time')]
        if completed_tickets_with_time:
            avg_completion_time = sum(t['completion_time'] for t in completed_tickets_with_time) / len(completed_tickets_with_time)
        else:
            avg_completion_time = 0
        
        return {
            'total_tickets': total_tickets,
            'completed_tickets': completed_tickets,
            'in_progress_tickets': in_progress_tickets,
            'backlog_tickets': backlog_tickets,
            'completion_rate': completed_tickets / total_tickets if total_tickets > 0 else 0,
            'utilization_rate': utilization_rate,
            'avg_completion_time': avg_completion_time,
            'timestamp': datetime.datetime.now().isoformat()
        }