# cli_interface.py
import datetime
import os
import zipfile
import re

class SmartSprintCLI:
    def __init__(self, system):
        self.system = system
        self.current_user = None
    
    def display_menu(self):
        print("\n" + "="*60)
        print("SMART SPRINT - AI-Enhanced Kanban Solution")
        print("="*60)
        print("1. View all tickets")
        print("2. View all developers")
        print("3. Process new feature story")
        print("4. Get recommendations, estimate timeline, and assign developer")
        print("5. Complete ticket")
        print("6. View system status")
        print("7. View developer performance (with historical data)")
        print("8. Process document")
        print("9. Process sprint document with user stories")
        print("10. Save data manually")
        print("11. Exit")
        
        # Show ML status
        self.system.check_ml_status()
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-11): ")
            
            if choice == '1':
                self.view_tickets()
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.view_developers()
                input("\nPress Enter to continue...")
            elif choice == '3':
                self.process_feature_story()
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.recommend_and_assign_ticket()
                input("\nPress Enter to continue...")
            elif choice == '5':
                self.complete_ticket()
                input("\nPress Enter to continue...")
            elif choice == '6':
                self.view_system_status()
                input("\nPress Enter to continue...")
            elif choice == '7':
                self.view_developer_performance()
                input("\nPress Enter to continue...")
            elif choice == '8':
                self.process_document()
                input("\nPress Enter to continue...")
            elif choice == '9':
                self.process_sprint_document_with_stories()
                input("\nPress Enter to continue...")
            elif choice == '10':
                self.system.manual_save()
                input("\nPress Enter to continue...")
            elif choice == '11':
                print("Saving data before exit...")
                self.system.save_data_to_csv()
                print("Exiting Smart Sprint system...")
                break
            else:
                print("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
    
    def view_tickets(self):
        print("\n" + "-"*30)
        print("TICKETS")
        print("-"*30)
        
        tickets_per_page = 5
        total_tickets = len(self.system.tickets)
        current_page = 0
        
        while True:
            start_idx = current_page * tickets_per_page
            end_idx = min(start_idx + tickets_per_page, total_tickets)
            
            print(f"\nShowing tickets {start_idx + 1}-{end_idx} of {total_tickets}:")
            
            for i in range(start_idx, end_idx):
                ticket = self.system.tickets[i]
                print(f"ID: {ticket['id']}")
                print(f"Title: {ticket['title']}")
                print(f"Priority: {ticket['priority']}")
                print(f"Complexity: {ticket['complexity']}")
                print(f"Status: {ticket['status']}")
                print(f"Estimated Hours: {ticket['estimated_hours']}")
                
                # Show assigned developer name and status
                if ticket.get('assigned_to') is not None:
                    dev = next((d for d in self.system.developers if d['id'] == ticket['assigned_to']), None)
                    if dev:
                        print(f"Assigned to: {dev['name']} (Status: {ticket['status']})")
                    else:
                        print(f"Assigned to: Unknown Developer (Status: {ticket['status']})")
                
                print(f"Tasks: {', '.join(ticket['tasks'])}")
                print("-"*20)
            
            # Navigation options
            total_pages = (total_tickets + tickets_per_page - 1) // tickets_per_page
            
            print(f"\nPage {current_page + 1} of {total_pages}")
            print("Options: n=next, p=previous, q=quit")
            
            choice = input("Enter choice: ").lower()
            
            if choice == 'n':
                if current_page < total_pages - 1:
                    current_page += 1
                else:
                    print("Already on the last page.")
            elif choice == 'p':
                if current_page > 0:
                    current_page -= 1
                else:
                    print("Already on the first page.")
            elif choice == 'q':
                break
            else:
                print("Invalid choice.")
    
    def view_developers(self):
        print("\n" + "-"*30)
        print("DEVELOPERS")
        print("-"*30)
        for dev in self.system.developers:
            print(f"ID: {dev['id']}")
            print(f"Name: {dev['name']}")
            # Print skills as a comma-separated string of words
            print(f"Skills: {', '.join(dev['skills'])}")
            print(f"Experience Level: {dev.get('experience_level', 'N/A')}")
            print(f"Availability: {dev['availability']} hours")
            print(f"Current Workload: {dev['current_workload']} hours")
            
            # Calculate utilization and handle overallocation
            utilization = dev['current_workload'] / dev['availability'] * 100 if dev['availability'] > 0 else 0
            if utilization > 100:
                print(f"Utilization: {utilization:.1f}% (OVERALLOCATED)")
            else:
                print(f"Utilization: {utilization:.1f}%")
            print("-"*20)
    
    def process_feature_story(self):
        print("\n" + "-"*30)
        print("PROCESS NEW FEATURE STORY")
        print("-"*30)
        
        title = input("Enter feature title: ")
        description = input("Enter feature description: ")
        priority = input("Enter priority (high/medium/low): ")
        estimated_hours = float(input("Enter estimated hours: "))
        
        feature_story = {
            "title": title,
            "description": description,
            "priority": priority,
            "estimated_hours": estimated_hours
        }
        
        ticket = self.system.process_feature_story(feature_story)
        print(f"\nFeature story processed successfully!")
        print(f"Generated Ticket ID: {ticket['id']}")
        print(f"Tasks: {', '.join(ticket['tasks'])}")
        print(f"Complexity: {ticket['complexity']}")
    
    def recommend_and_assign_ticket(self):
        print("\n" + "-"*30)
        print("RECOMMEND, ESTIMATE, AND ASSIGN TICKET")
        print("-"*30)
        
        ticket_id = int(input("Enter ticket ID: "))
        
        # Check if the ticket exists
        ticket = next((t for t in self.system.tickets if t['id'] == ticket_id), None)
        if not ticket:
            print(f"Error: Ticket with ID {ticket_id} not found.")
            print("Available ticket IDs:")
            for t in self.system.tickets[:10]:  # Show first 10 tickets
                print(f"  ID: {t['id']}, Title: {t['title']}")
            if len(self.system.tickets) > 10:
                print("  ... and more")
            return
        
        # Check if ticket is already assigned or completed
        if ticket['status'] == 'completed':
            print(f"This ticket is already completed.")
            return
        
        if ticket.get('assigned_to') is not None:
            dev = next((d for d in self.system.developers if d['id'] == ticket['assigned_to']), None)
            if dev:
                print(f"This ticket is already assigned to {dev['name']} (Status: {ticket['status']}).")
                reassign = input("Would you like to reassign it to a different developer? (y/n): ").lower()
                if reassign != 'y':
                    return
        
        # Get recommendations
        recommendations = self.system.get_ticket_recommendations(ticket_id)
        
        if not recommendations:
            print("No recommendations found.")
            print("This could be because:")
            print("1. No developers have the required skills")
            print("2. All developers are fully booked")
            print("3. There's an issue with the recommendation algorithm")
            return
        
        print(f"\nTicket: {ticket['title']}")
        print("Recommended Developers (with historical performance):")
        
        for i, rec in enumerate(recommendations, 1):
            dev = next((d for d in self.system.developers if d['id'] == rec['developer_id']), None)
            if dev:
                availability = dev['availability'] - dev['current_workload']
                # Format availability to show negative values in parentheses
                availability_str = f"{availability} hours" if availability >= 0 else f"({abs(availability)} hours overallocated)"
                print(f"{i}. {dev['name']} (ID: {dev['id']})")
                print(f"   Skills: {', '.join(dev['skills'])}")
                print(f"   Match Score: {rec['match_score']:.2f}")
                print(f"   Availability: {availability_str}")
                print(f"   Experience Level: {dev.get('experience_level', 'N/A')}")
                
                # Check if skills_match has data before trying to access it
                if rec['skills_match']:
                    print(f"   Historical Performance:")
                    print(f"     Velocity: {rec['skills_match'].get('velocity', 'N/A'):.2f}")
                    print(f"     Accuracy: {rec['skills_match'].get('accuracy', 'N/A'):.2f}")
                    print(f"     Sentiment: {rec['skills_match'].get('sentiment', 'N/A'):.2f}")
                else:
                    print("   Historical Performance: No data available")
        
        # Ask if user wants to see timeline for top recommendation
        show_timeline = input("\nWould you like to see the estimated timeline for the top recommended developer? (y/n): ").lower()
        if show_timeline == 'y' and recommendations:
            top_dev_id = recommendations[0]['developer_id']
            top_dev = next((d for d in self.system.developers if d['id'] == top_dev_id), None)
            
            if top_dev:
                # Get timeline estimate
                estimate = self.system.training_module.estimate_timeline(ticket, top_dev, 
                                                                      self.system.performance_tracker.get_historical_performance_data())
                
                if estimate:
                    print(f"\nTimeline estimate for {top_dev['name']}:")
                    print(f"Estimated Hours: {ticket['estimated_hours']}")
                    print(f"Complexity Level: {ticket['complexity']}")
                    print(f"Mean Duration: {estimate['mean_duration']:.1f} hours")
                    print(f"80th Percentile: {estimate['p80_duration']:.1f} hours")
                    print(f"Risk Level: {estimate['risk_level']}")
                    print(f"Confidence Interval: {estimate['confidence_interval'][0]:.1f} - {estimate['confidence_interval'][1]:.1f} hours")
        
        # Ask if user wants to assign the ticket
        assign = input("\nWould you like to assign this ticket to a developer? (y/n): ").lower()
        if assign == 'y':
            # Let user choose a developer
            choice = input("Select a developer (number) or enter 0 to cancel: ")
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    return
                elif 1 <= choice_num <= len(recommendations):
                    developer_id = recommendations[choice_num-1]['developer_id']
                    # Assign the selected developer
                    if self.system.assign_developer_to_ticket(ticket_id, developer_id):
                        dev = next((d for d in self.system.developers if d['id'] == developer_id), None)
                        print(f"Developer {dev['name']} assigned to ticket '{ticket['title']}'")
                    else:
                        print("Assignment failed. The developer may not have enough availability for this ticket.")
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(recommendations)} or 0 to cancel.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def complete_ticket(self):
        print("\n" + "-"*30)
        print("COMPLETE TICKET")
        print("-"*30)
        
        ticket_id = int(input("Enter ticket ID: "))
        completion_time = float(input("Enter actual completion time (hours): "))
        revisions = int(input("Enter number of revisions: "))
        sentiment_score = float(input("Enter sentiment score (0-1): "))
        
        if self.system.complete_ticket(ticket_id, completion_time, revisions, sentiment_score):
            print("Ticket completed successfully!")
            ticket = next((t for t in self.system.tickets if t['id'] == ticket_id), None)
            if ticket:
                print(f"Ticket '{ticket['title']}' marked as completed")
        else:
            print("Completion failed. Check if ticket exists and is assigned.")
    
    def view_system_status(self):
        status = self.system.get_system_status()
        print("\n" + "-"*30)
        print("SYSTEM STATUS")
        print("-"*30)
        print(f"Total Tickets: {status['total_tickets']}")
        print(f"  - Completed: {status['completed_tickets']}")
        print(f"  - In Progress: {status['in_progress_tickets']}")
        print(f"  - Backlog: {status['backlog_tickets']}")
        print(f"Total Workload: {status['total_workload']} hours")
        print(f"Total Availability: {status['total_availability']} hours")
        print(f"Utilization Rate: {status['utilization_rate']:.1f}%")
    
    def view_developer_performance(self):
        print("\n" + "-"*30)
        print("DEVELOPER PERFORMANCE (WITH HISTORICAL DATA)")
        print("-"*30)
        
        developer_id = int(input("Enter developer ID: "))
        performance = self.system.get_developer_performance(developer_id)
        
        if not performance:
            print("No performance data found for this developer.")
            return
        
        dev = next((d for d in self.system.developers if d['id'] == developer_id), None)
        if dev:
            print(f"Developer: {dev['name']}")
            print(f"Average Completion Time: {performance['average_completion_time']:.1f} hours")
            print(f"Accuracy: {performance['accuracy']:.2f}")
            print(f"Total Completed Tickets: {performance['total_completed_tickets']}")
            print(f"Average Sentiment: {performance['average_sentiment']:.2f}")
            
            hist_perf = performance['historical_performance']
            print(f"\nHistorical Performance Summary:")
            print(f"  Velocity: {hist_perf.get('velocity', 'N/A'):.2f}")
            print(f"  Accuracy: {hist_perf.get('accuracy', 'N/A'):.2f}")
            print(f"  Sentiment: {hist_perf.get('sentiment', 'N/A'):.2f}")
            print(f"  Tickets Completed: {hist_perf.get('tickets_completed', 'N/A')}")
    
    def process_document(self):
        """Process a Word document to extract tasks"""
        print("\n" + "-"*30)
        print("PROCESS DOCUMENT")
        print("-"*30)
        
        doc_path = input("Enter document path: ")
        
        if not os.path.exists(doc_path):
            print(f"Error: File not found at {doc_path}")
            return
        
        try:
            from sprint_document_processor import SprintDocumentProcessor
            processor = SprintDocumentProcessor()
            
            print(f"Processing document: {doc_path}")
            
            if doc_path.lower().endswith('.docx'):
                if not self._is_valid_docx(doc_path):
                    print("Warning: This doesn't appear to be a valid .docx file.")
                    print("It might be in the older .doc format or corrupted.")
                    convert = input("Would you like to try processing it as text anyway? (y/n): ").lower()
                    if convert != 'y':
                        print("Please try saving the document as a .docx or .txt file and try again.")
                        return
                    tasks = self._process_as_text(doc_path)
                else:
                    try:
                        import docx
                        tasks = processor.process_document(doc_path)
                    except ImportError:
                        print("Error: python-docx library is not installed.")
                        print("Please install it using: pip install python-docx")
                        return
                    except Exception as e:
                        print(f"Error processing .docx file: {e}")
                        print("Would you like to try processing it as text? (y/n)")
                        if input().lower() == 'y':
                            tasks = self._process_as_text(doc_path)
                        else:
                            return
            elif doc_path.lower().endswith('.txt'):
                tasks = processor.process_text_document(doc_path)
            elif doc_path.lower().endswith('.doc'):
                print("Detected .doc format. Converting to text...")
                tasks = self._process_as_text(doc_path)
            else:
                print("Error: Only .docx, .doc, and .txt files are supported")
                return
            
            print(f"\nFound {len(tasks)} tasks in document:")
            for i, task in enumerate(tasks, 1):
                print(f"\nTask {i}:")
                print(f"  Title: {task['title']}")
                print(f"  Description: {task['description'][:100]}...")
                print(f"  Priority: {task['priority']}")
                print(f"  Estimated Hours: {task['estimated_hours']}")
            
            add_to_system = input("\nAdd these tasks to the system? (y/n): ").lower()
            if add_to_system == 'y':
                for task in tasks:
                    feature_story = {
                        "title": task['title'],
                        "description": task['description'],
                        "priority": task['priority'],
                        "estimated_hours": task['estimated_hours']
                    }
                    self.system.process_feature_story(feature_story)
                print("Tasks added to system successfully!")
            else:
                print("Tasks not added to system.")
                
        except Exception as e:
            print(f"Error processing document: {e}")
            print("Possible solutions:")
            print("1. Check if the file is in .docx format (not .doc)")
            print("2. Try creating a new .docx file with the same content")
            print("3. Try saving the document as a plain text (.txt) file")
            print("4. Check if the file is corrupted or password-protected")
            print("5. Make sure python-docx library is installed (pip install python-docx)")
    
    def process_sprint_document_with_stories(self):
        """Process a sprint document with sprint goal and user stories, and generate tasks"""
        print("\n" + "-"*30)
        print("PROCESS SPRINT DOCUMENT WITH USER STORIES")
        print("-"*30)
        
        doc_path = input("Enter document path: ")
        
        # Validate file exists
        if not os.path.exists(doc_path):
            print(f"Error: File not found at {doc_path}")
            return
        
        try:
            from sprint_document_processor import SprintDocumentProcessor
            processor = SprintDocumentProcessor()
            
            print(f"Processing sprint document: {doc_path}")
            
            # Process the sprint document
            sprint_data = processor.process_sprint_document_with_stories(doc_path)
            
            if not sprint_data:
                print("Failed to process the sprint document.")
                return
            
            # Display sprint goal
            print(f"\nSprint Goal: {sprint_data['sprint_goal']}")
            
            # Display user stories
            print("\nUser Stories:")
            for i, story in enumerate(sprint_data['user_stories'], 1):
                print(f"{i}. {story['story']} (Story Points: {story['story_points']})")
            
            # Display generated tasks
            print("\nGenerated Tasks:")
            for i, task in enumerate(sprint_data['tasks'], 1):
                print(f"{i}. {task['title']}")
                print(f"   Priority: {task['priority']}, Estimated Hours: {task['estimated_hours']}")
            
            # Ask if user wants to add tasks to system
            add_to_system = input("\nAdd these tasks to the system? (y/n): ").lower()
            if add_to_system == 'y':
                for task in sprint_data['tasks']:
                    feature_story = {
                        "title": task['title'],
                        "description": task['description'],
                        "priority": task['priority'],
                        "estimated_hours": task['estimated_hours']
                    }
                    ticket = self.system.process_feature_story(feature_story)
                    print(f"Created ticket: {ticket['id']} - {ticket['title']}")
            
                print("Tasks added to system successfully!")
            else:
                print("Tasks not added to system.")
                
        except Exception as e:
            print(f"Error processing sprint document: {e}")
    
    def _is_valid_docx(self, doc_path):
        try:
            with zipfile.ZipFile(doc_path, 'r') as zip_ref:
                required_files = ['[Content_Types].xml', 'word/document.xml']
                for file in required_files:
                    if file not in zip_ref.namelist():
                        return False
                return True
        except (zipfile.BadZipFile, Exception):
            return False
    
    def _process_as_text(self, doc_path):
        try:
            with open(doc_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            
            if doc_path.lower().endswith('.doc'):
                print("Note: .doc files may not convert perfectly to text.")
                print("For best results, save the document as .docx or .txt format.")
            
            task_pattern = r'Task\s+\d+[:\s]*(.*?)(?=Task\s+\d+[:\s]*|$)'
            matches = re.findall(task_pattern, text_content, re.DOTALL)
            
            tasks = []
            for i, match in enumerate(matches):
                task_text = match.strip()
                
                lines = task_text.split('\n')
                title = lines[0].strip()
                description = '\n'.join(lines[1:]).strip()
                
                if not title:
                    title = f"Task {i+1}"
                
                priority = 'medium'
                estimated_hours = 16
                
                tasks.append({
                    'title': title,
                    'description': description,
                    'priority': priority,
                    'estimated_hours': estimated_hours
                })
            
            return tasks
            
        except Exception as e:
            print(f"Error reading file as text: {e}")
            print("Please try saving the document as a .txt file and try again.")
            return []