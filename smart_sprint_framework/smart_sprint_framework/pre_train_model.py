import os
import sys
from smart_sprint_system import SmartSprintSystem
def main():
    print("Smart Sprint Model Pre-training")
    print("=" * 50)
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
        print("Created models directory.")
    
    # Initialize the system with large dataset
    print("Initializing system with large dataset...")
    system = SmartSprintSystem()
    
    # Modify the system to load the large dataset
    system._load_large_dataset_for_training()
    
    # Get historical data
    historical_data = system.performance_tracker.get_historical_performance_data()
    
    # Check if we have enough data
    completed_tickets = [t for t in system.tickets if t.get('status') == 'completed']
    
    if len(completed_tickets) < 10:
        print(f"Not enough completed tickets ({len(completed_tickets)}) for training. Need at least 10.")
        print("This should not happen with the generated dataset.")
        return
    
    # Train models
    print(f"Training models with {len(completed_tickets)} completed tickets...")
    training_module = TrainingModule()
    success = training_module.train_models(system.tickets, system.developers, historical_data)
    
    if success:
        # Save models
        training_module.save_models()
        print("\nModels trained and saved successfully!")
        
        # Now generate the small dataset for the actual system
        print("\nGenerating small dataset for the system...")
        from generate_small_dataset import generate_small_developers_csv, generate_small_sprint_documents_csv, generate_small_performance_data
        generate_small_developers_csv()
        generate_small_sprint_documents_csv()
        generate_small_performance_data()
        print("Small dataset generated successfully.")
        
        print("\nPre-training completed successfully!")
        print("The system is now ready with pre-trained models and a small dataset.")
    else:
        print("\nFailed to train models.")
if __name__ == "__main__":
    main()