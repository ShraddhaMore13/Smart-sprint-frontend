import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Setup and run Smart Sprint System')
    parser.add_argument('--regenerate', action='store_true', 
                        help='Regenerate data files (WARNING: This will overwrite existing data)')
    args = parser.parse_args()
    
    print("Setting up Smart Sprint System...")
    
    # Check if data files exist
    files_exist = all([
        os.path.exists('developers_small.csv'),
        os.path.exists('sprint_documents_small.csv'),
        os.path.exists('performance_data_small.csv')
    ])
    
    # Only regenerate if explicitly requested or if files don't exist
    if args.regenerate or not files_exist:
        if args.regenerate:
            print("WARNING: Regenerating data files. All existing data will be lost.")
            confirm = input("Are you sure you want to continue? (y/n): ")
            if confirm.lower() != 'y':
                print("Data regeneration cancelled.")
                return
        
        print("Generating sample data...")
        try:
            # Run the data generation script
            subprocess.run([sys.executable, 'generate_small_dataset.py'], check=True)
            print("Data files generated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error generating data files: {e}")
            return
    else:
        print("Using existing data files.")
    
    # Start the Flask backend
    print("Starting Smart Sprint backend...")
    try:
        backend_process = subprocess.Popen([sys.executable, 'app.py'])
        print(f"Backend started with PID: {backend_process.pid}")
        
        # Wait for user to stop the backend
        input("Press Enter to stop the backend...")
        
        # Terminate the backend process
        backend_process.terminate()
        backend_process.wait()
        print("Backend stopped.")
    except Exception as e:
        print(f"Error starting backend: {e}")

if __name__ == "__main__":
    main()