import os
import sys
import subprocess
def main():
    print("Smart Sprint Setup and Run")
    print("=" * 50)
    
    # Only regenerate the small dataset if it doesn't exist
    if not os.path.exists('developers_small.csv') or not os.path.exists('sprint_documents_small.csv') or not os.path.exists('performance_data_small.csv'):
        print("Small dataset not found. Regenerating...")
        subprocess.run([sys.executable, 'generate_small_dataset.py'], check=True)
        print("Small dataset regenerated.")
    else:
        print("Small dataset found. Skipping regeneration.")
    
    print("\nStarting Smart Sprint system...")
    # Run the Flask app
    subprocess.run([sys.executable, 'app.py'])

if __name__ == "__main__":
    main()