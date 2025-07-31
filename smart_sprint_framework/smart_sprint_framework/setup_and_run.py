import os
import sys
import subprocess
from main import main as run_main

def main():
    print("Smart Sprint Setup and Run")
    print("=" * 50)
    
    # Check if models directory exists
    if not os.path.exists('models'):
        print("Models directory not found. Running pre-training...")
        subprocess.run([sys.executable, 'pre_train_model.py'], check=True)
        print("Pre-training completed.")
    else:
        print("Models directory found. Skipping pre-training.")
    
    # Only regenerate the small dataset if it doesn't exist
    if not os.path.exists('developers_small.csv') or not os.path.exists('sprint_documents_small.csv') or not os.path.exists('performance_data_small.csv'):
        print("Small dataset not found. Regenerating...")
        subprocess.run([sys.executable, 'generate_small_dataset_only.py'], check=True)
        print("Small dataset regenerated.")
    else:
        print("Small dataset found. Skipping regeneration.")
    
    print("\nStarting Smart Sprint system...")
    run_main()

if __name__ == "__main__":
    main()