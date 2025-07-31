import requests
import json
from requests.auth import HTTPBasicAuth

class JiraIntegration:
    def __init__(self, url, username, api_token):
        self.url = url
        self.auth = HTTPBasicAuth(username, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def create_ticket(self, ticket_data):
        """Create a ticket in Jira from Smart Sprint ticket data"""
        jira_ticket = {
            "fields": {
                "project": {
                    "key": ticket_data.get('project_key', 'SS')
                },
                "summary": ticket_data['title'],
                "description": ticket_data['description'],
                "issuetype": {
                    "name": "Task"
                },
                "priority": {
                    "name": ticket_data['priority'].capitalize()
                },
                "timetracking": {
                    "originalEstimate": f"{ticket_data['estimated_hours']}h"
                }
            }
        }
        
        if ticket_data.get('assigned_to'):
            jira_ticket["fields"]["assignee"] = {"name": ticket_data['assigned_to']}
        
        try:
            response = requests.post(
                f"{self.url}/rest/api/2/issue",
                json=jira_ticket,
                headers=self.headers,
                auth=self.auth
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                return {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def update_ticket_status(self, jira_id, status):
        """Update ticket status in Jira"""
        transition_url = f"{self.url}/rest/api/2/issue/{jira_id}/transitions"
        
        # Get available transitions
        try:
            response = requests.get(
                f"{self.url}/rest/api/2/issue/{jira_id}/transitions?expand=transitions.fields",
                headers=self.headers,
                auth=self.auth
            )
            
            if response.status_code == 200:
                transitions = response.json()['transitions']
                target_transition = None
                
                for t in transitions:
                    if status.lower() in t['name'].lower():
                        target_transition = t
                        break
                
                if target_transition:
                    transition_data = {
                        "transition": {
                            "id": target_transition['id']
                        }
                    }
                    
                    response = requests.post(
                        transition_url,
                        json=transition_data,
                        headers=self.headers,
                        auth=self.auth
                    )
                    
                    return response.status_code == 204
            return False
        except Exception as e:
            print(f"Error updating ticket status: {e}")
            return False
    
    def add_comment(self, jira_id, comment):
        """Add a comment to a Jira ticket"""
        try:
            response = requests.post(
                f"{self.url}/rest/api/2/issue/{jira_id}/comment",
                json={"body": comment},
                headers=self.headers,
                auth=self.auth
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error adding comment: {e}")
            return False