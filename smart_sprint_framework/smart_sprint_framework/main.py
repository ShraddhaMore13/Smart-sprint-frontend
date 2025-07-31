# main.py
import os
from smart_sprint_system import SmartSprintSystem
from cli_interface import SmartSprintCLI

def main():
    print("Smart Sprint - AI-Enhanced Kanban Solution")
    print("=" * 50)
    print("Initializing system...")
    
    # Initialize the system
    system = SmartSprintSystem()
    
    # Create CLI interface
    cli = SmartSprintCLI(system)
    
    print("System initialized successfully!")
    print("Starting CLI interface...")
    
    # Start the CLI
    cli.run()

if __name__ == "__main__":
    main()