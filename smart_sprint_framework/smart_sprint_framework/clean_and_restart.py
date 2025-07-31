# clean_and_restart.py
import os
import subprocess

def main():
    print("Cleaning up existing data files...")
    
    # Remove existing small dataset files
    files_to_remove = [
        'developers_small.csv',
        'sprint_documents_small.csv',
        'performance_data_small.csv'
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed {file}")
    
    # Regenerate the small dataset
    print("\nRegenerating small dataset...")
    subprocess.run([sys.executable, 'generate_small_dataset_only.py'], check=True)
    
    print("\nCleanup and regeneration completed.")
    print("You can now run 'python setup_and_run.py' to start the system with a fresh dataset.")

if __name__ == "__main__":
    import sys
    main()