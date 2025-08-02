import datetime
class PerformanceTracker:
    def __init__(self):
        self.metrics = []
    
    def track_performance(self, developer_id, ticket_id, completion_time, revisions, sentiment_score):
        metric = {
            'developer_id': developer_id,
            'ticket_id': ticket_id,
            'completion_time': completion_time,
            'revisions': revisions,
            'sentiment_score': sentiment_score,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self.metrics.append(metric)
        return metric
    
    def get_developer_metrics(self, developer_id):
        return [m for m in self.metrics if m['developer_id'] == developer_id]
    
    def calculate_velocity(self, developer_id):
        metrics = self.get_developer_metrics(developer_id)
        if not metrics:
            return 0
        
        total_time = sum(m['completion_time'] for m in metrics)
        return total_time / len(metrics)
    
    def calculate_accuracy(self, developer_id):
        metrics = self.get_developer_metrics(developer_id)
        if not metrics:
            return 0
        
        total_revisions = sum(m['revisions'] for m in metrics)
        return 1.0 / (1.0 + total_revisions * 0.1)
    
    def get_historical_performance_data(self):
        performance_summary = {}
        
        for dev_id in set(m['developer_id'] for m in self.metrics):
            metrics = self.get_developer_metrics(dev_id)
            if metrics:
                performance_summary[dev_id] = {
                    'velocity': self.calculate_velocity(dev_id),
                    'accuracy': self.calculate_accuracy(dev_id),
                    'sentiment': sum(m['sentiment_score'] for m in metrics) / len(metrics),
                    'tickets_completed': len(metrics)
                }
        
        return performance_summary