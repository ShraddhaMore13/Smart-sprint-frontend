# monte_carlo.py
import numpy as np

class MonteCarloEstimator:
    def __init__(self):
        self.complexity_factors = {
            1: (0.8, 1.2),
            2: (0.7, 1.3),
            3: (0.6, 1.4),
            4: (0.5, 1.5),
            5: (0.4, 1.6)
        }
    
    def estimate_task_duration(self, estimated_hours, complexity):
        min_factor, max_factor = self.complexity_factors[complexity]
        
        simulations = []
        for _ in range(1000):
            factor = np.random.uniform(min_factor, max_factor)
            simulated_hours = estimated_hours * factor
            simulations.append(simulated_hours)
        
        mean_duration = np.mean(simulations)
        std_duration = np.std(simulations)
        p80 = np.percentile(simulations, 80)
        
        return {
            'estimated_hours': estimated_hours,
            'complexity': complexity,
            'mean_duration': mean_duration,
            'std_duration': std_duration,
            'p80_duration': p80,
            'confidence_interval': (np.percentile(simulations, 5), np.percentile(simulations, 95)),
            'risk_level': 'low' if p80 < estimated_hours * 1.3 else 'medium' if p80 < estimated_hours * 1.5 else 'high'
        }
