# train_models.py
import os
import sys
from smart_sprint_system import SmartSprintSystem

def main():
    print("Smart Sprint Model Training")
    print("=" * 50)
    
    # Initialize the system
    system = SmartSprintSystem()
    
    # Get historical data
    historical_data = system.performance_tracker.get_historical_performance_data()
    
    # Check if we have enough data
    completed_tickets = [t for t in system.tickets if t.get('status') == 'completed']
    
    if len(completed_tickets) < 10:
        print(f"Not enough completed tickets ({len(completed_tickets)}) for training. Need at least 10.")
        print("Please complete more tickets and try again.")
        return
    
    # Train models
    print(f"Training models with {len(completed_tickets)} completed tickets...")
    success = system.training_module.train_models(system.tickets, system.developers, historical_data)
    
    if success:
        # Save models
        system.training_module.save_models()
        print("\nModels trained and saved successfully!")
    else:
        print("\nFailed to train models.")

if __name__ == "__main__":
    main()