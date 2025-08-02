import pandas as pd
import os

def fix_ticket_ids():
    # Check if files exist
    if not os.path.exists('sprint_documents_small.csv'):
        print("sprint_documents_small.csv not found!")
        return False
    
    if not os.path.exists('performance_data_small.csv'):
        print("performance_data_small.csv not found!")
        return False
    
    # Load tickets
    try:
        tickets_df = pd.read_csv('sprint_documents_small.csv')
        print(f"Loaded {len(tickets_df)} tickets")
        
        # Create a mapping of old IDs to new sequential IDs
        old_ids = tickets_df['id'].tolist()
        id_mapping = {old_id: new_id for new_id, old_id in enumerate(sorted(old_ids), 1)}
        
        # Apply new IDs
        tickets_df['id'] = tickets_df['id'].map(id_mapping)
        
        # Save updated tickets
        tickets_df.to_csv('sprint_documents_small.csv', index=False)
        print("Updated ticket IDs in sprint_documents_small.csv")
        
        # Load performance data
        perf_df = pd.read_csv('performance_data_small.csv')
        print(f"Loaded {len(perf_df)} performance records")
        
        # Update ticket IDs in performance data
        perf_df['ticket_id'] = perf_df['ticket_id'].map(id_mapping)
        
        # Save updated performance data
        perf_df.to_csv('performance_data_small.csv', index=False)
        print("Updated ticket IDs in performance_data_small.csv")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Fixing ticket IDs to start from 1...")
    if fix_ticket_ids():
        print("Ticket IDs fixed successfully!")
    else:
        print("Failed to fix ticket IDs.")