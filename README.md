Smart Sprint: AI-Enhanced Kanban Solution for Agile Teams

Software Requirements:
- Python: 3.8 or higher
- Node.js: 14.0 or higher
- npm: 6.0 or higher

Python Libraries :pip install flask flask-cors pandas numpy scikit-learn joblib python-jwt docx
Node.js Packages : npm install react react-dom axios

Project Structure :
smart_sprint_framework/
├── app.py                           Main Flask application
├── auth.py                          Authentication module
├── error_handler.py                  Custom error handling
├── smart_sprint_system.py            Core system class
├── setup_and_run.py                 Setup script
├── requirements.txt                  Python dependencies
├── jira_config.json                 Jira configuration (optional)
├── models/                           Trained ML models directory
├── backups/                         Data backup directory
├── developers_small.csv             Sample developers data
├── sprint_documents_small.csv       Sample tickets data
├── performance_data_small.csv       Sample performance data
├── frontend/                        React frontend
│   ├── public/
│   ├── src/
│   │   ├── App.jsx                 Main React component
│   │   ├── Dashboard.jsx           Dashboard component
│   │   └── App.css                 Application styles
│   └── package.json
└── README.md                        This file


 Setup Instructions:
1. Clone the Repository:
 2.Install python and nodejs packages.
3. Open 2 Terminals –

1) Start Backend Server:
 Navigate to  smart_sprint_framework directory and run setup_and_run.py 
This command will:
- Generate sample CSV files (developers, tickets, performance data)
- Train machine learning models
- Start the Flask backend
Then run - python app.py: 
The backend will start on `http://localhost:5001

2) Start Frontend Development Server:
 Navigate to  frontend directory and run npm start
The frontend will be available at `http://localhost:3000`

 Access the Application:

Open a web browser and navigate to `http://localhost:3000`
  Login Credentials - Admin: username: `admin`, password: `admin123`
   - User: username: `user`, password: `user123`
Functionality:
1. Login: Use the credentials above
2. Dashboard: View project metrics and visualizations
3. Ticket Management: Create, assign, and complete tickets
4. Document Processing: Upload Word/text documents to extract tasks
5. Developer Assignment: Get AI-powered recommendations
6. Performance Tracking: Monitor developer metrics and bottlenecks

 





