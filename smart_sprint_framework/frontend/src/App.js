import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './Dashboard';

function App() {
    const [tickets, setTickets] = useState([]);
    const [developers, setDevelopers] = useState([]);
    const [systemStatus, setSystemStatus] = useState({});
    const [loading, setLoading] = useState(true);
    const [activeView, setActiveView] = useState('dashboard');
    const [selectedTicket, setSelectedTicket] = useState(null);
    const [selectedDeveloper, setSelectedDeveloper] = useState(null);
    const [developerPerformance, setDeveloperPerformance] = useState(null);
    const [newTicket, setNewTicket] = useState({
        title: '',
        description: '',
        priority: 'medium',
        estimated_hours: 8
    });
    const [completeTicketData, setCompleteTicketData] = useState({
        completion_time: 10,
        revisions: 0,
        sentiment_score: 0.8
    });
    const [documentPath, setDocumentPath] = useState('');
    const [sprintDocumentPath, setSprintDocumentPath] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [timeline, setTimeline] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('token'));

    useEffect(() => {
        if (isAuthenticated) {
            fetchInitialData();
        }
    }, [isAuthenticated]);

    useEffect(() => {
        if (token) {
            // Verify token with a simple request
            fetch('http://localhost:5000/api/tickets', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            })
                .then(response => {
                    if (response.ok) {
                        setIsAuthenticated(true);
                        // Extract username from token (in a real app, you'd decode the JWT)
                        setUser({ username: 'user', role: 'user' }); // Simplified for this example
                    } else {
                        localStorage.removeItem('token');
                        setToken(null);
                    }
                })
                .catch(error => {
                    console.error('Token verification error:', error);
                    localStorage.removeItem('token');
                    setToken(null);
                });
        }
    }, [token]);

    const fetchInitialData = async () => {
        if (!isAuthenticated) return;

        try {
            const [ticketsResponse, developersResponse, statusResponse] = await Promise.all([
                apiRequest('http://localhost:5000/api/tickets'),
                apiRequest('http://localhost:5000/api/developers'),
                apiRequest('http://localhost:5000/api/system/status')
            ]);
            const ticketsData = await ticketsResponse.json();
            const developersData = await developersResponse.json();
            const statusData = await statusResponse.json();

            // Remove duplicate tickets based on title
            const uniqueTickets = removeDuplicateTickets(ticketsData);
            setTickets(uniqueTickets);
            setDevelopers(developersData);
            setSystemStatus(statusData);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            if (error.response && error.response.status === 401) {
                // Token expired or invalid
                logout();
                alert('Session expired. Please login again.');
            }
            setLoading(false);
        }
    };

    const apiRequest = async (url, options = {}) => {
        const headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
        };

        return fetch(url, {
            ...options,
            headers,
        });
    };

    const login = async (username, password) => {
        try {
            const response = await fetch('http://localhost:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                const data = await response.json();
                setToken(data.token);
                setUser({ username: data.username, role: data.role });
                setIsAuthenticated(true);
                localStorage.setItem('token', data.token);
                return true;
            } else {
                const error = await response.json();
                alert(error.error || 'Login failed');
                return false;
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed');
            return false;
        }
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        setIsAuthenticated(false);
        localStorage.removeItem('token');
    };

    const removeDuplicateTickets = (tickets) => {
        const seen = new Set();
        return tickets.filter(ticket => {
            const duplicate = seen.has(ticket.title);
            seen.add(ticket.title);
            return !duplicate;
        });
    };

    const fetchDeveloperPerformance = async (developerId) => {
        try {
            const response = await apiRequest(`http://localhost:5000/api/developers/${developerId}/performance`);
            if (response.ok) {
                const performanceData = await response.json();
                setDeveloperPerformance(performanceData);
            } else {
                setDeveloperPerformance(null);
            }
        } catch (error) {
            console.error('Error fetching developer performance:', error);
            setDeveloperPerformance(null);
        }
    };

    const handleCreateTicket = async (e) => {
        e.preventDefault();
        try {
            const response = await apiRequest('http://localhost:5000/api/tickets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newTicket),
            });
            if (response.ok) {
                const createdTicket = await response.json();
                setTickets([...tickets, createdTicket]);
                setNewTicket({
                    title: '',
                    description: '',
                    priority: 'medium',
                    estimated_hours: 8
                });
                setActiveView('dashboard');
                alert('Ticket created successfully!');
            }
        } catch (error) {
            console.error('Error creating ticket:', error);
            alert('Error creating ticket!');
        }
    };

    const handleAssignTicket = async (ticketId, developerId) => {
        try {
            const response = await apiRequest(`http://localhost:5000/api/tickets/${ticketId}/assign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ developer_id: developerId }),
            });
            if (response.ok) {
                // Refresh tickets to get updated status
                const ticketsResponse = await apiRequest('http://localhost:5000/api/tickets');
                const ticketsData = await ticketsResponse.json();
                const uniqueTickets = removeDuplicateTickets(ticketsData);
                setTickets(uniqueTickets);
                alert('Ticket assigned successfully!');
            }
        } catch (error) {
            console.error('Error assigning ticket:', error);
            alert('Error assigning ticket!');
        }
    };

    const handleCompleteTicket = async (ticketId) => {
        try {
            const response = await apiRequest(`http://localhost:5000/api/tickets/${ticketId}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(completeTicketData),
            });
            if (response.ok) {
                // Refresh tickets to get updated status
                const ticketsResponse = await apiRequest('http://localhost:5000/api/tickets');
                const ticketsData = await ticketsResponse.json();
                const uniqueTickets = removeDuplicateTickets(ticketsData);
                setTickets(uniqueTickets);
                setSelectedTicket(null);
                alert('Ticket completed successfully!');
            }
        } catch (error) {
            console.error('Error completing ticket:', error);
            alert('Error completing ticket!');
        }
    };

    const handleGetRecommendations = async (ticketId) => {
        try {
            const response = await apiRequest(`http://localhost:5000/api/tickets/${ticketId}/recommendations`);
            const recommendationsData = await response.json();
            setRecommendations(recommendationsData);
            // Also get timeline estimate
            const ticket = tickets.find(t => t.id === ticketId);
            if (ticket && recommendationsData.length > 0) {
                const developer = developers.find(d => d.id === recommendationsData[0].developer_id);
                if (developer) {
                    // For now, we'll use a simple timeline estimation
                    setTimeline({
                        estimated_hours: Math.ceil(ticket.estimated_hours),
                        complexity: ticket.complexity,
                        mean_duration: Math.ceil(ticket.estimated_hours * 1.2),
                        risk_level: 'medium'
                    });
                }
            }
        } catch (error) {
            console.error('Error getting recommendations:', error);
            alert('Error getting recommendations!');
        }
    };

    const handleSaveData = async () => {
        try {
            const response = await apiRequest('http://localhost:5000/api/system/save', {
                method: 'POST',
            });
            if (response.ok) {
                alert('Data saved successfully!');
            }
        } catch (error) {
            console.error('Error saving data:', error);
            alert('Error saving data!');
        }
    };

    const handleProcessDocument = async (e) => {
        if (!documentPath) {
            alert('Please enter a document path');
            return;
        }
        // Show loading state
        const originalButtonText = e.target.textContent;
        e.target.textContent = 'Processing...';
        e.target.disabled = true;
        try {
            const response = await apiRequest('http://localhost:5000/api/process-document', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ path: documentPath }),
            });
            const result = await response.json();
            if (response.ok && result.message === 'Document processed successfully') {
                alert(`Document processed successfully!\n\nTasks Extracted: ${result.tasks_extracted}\nTickets Created: ${result.tickets_created}`);
                // Refresh tickets to get new tickets
                fetchInitialData();
                // Clear the input field
                setDocumentPath('');
            } else {
                alert(result.message || 'Error processing document!');
            }
        } catch (error) {
            console.error('Error processing document:', error);
            alert('Error processing document! Please check the console for details.');
        } finally {
            // Reset button state
            e.target.textContent = originalButtonText;
            e.target.disabled = false;
        }
    };

    const handleProcessSprintDocument = async (e) => {
        if (!sprintDocumentPath) {
            alert('Please enter a sprint document path');
            return;
        }
        // Show loading state
        const originalButtonText = e.target.textContent;
        e.target.textContent = 'Processing...';
        e.target.disabled = true;
        try {
            const response = await apiRequest('http://localhost:5000/api/process-sprint-document', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ path: sprintDocumentPath }),
            });
            const result = await response.json();
            if (response.ok && result.message === 'Sprint document processed successfully') {
                alert(`Sprint document processed successfully!\n\nSprint Goal: ${result.sprint_goal}\nUser Stories: ${result.user_stories.length}\nTasks Created: ${result.tickets_created}`);
                // Refresh tickets to get new tickets
                fetchInitialData();
                // Clear the input field
                setSprintDocumentPath('');
            } else {
                alert(result.message || 'Error processing sprint document!');
            }
        } catch (error) {
            console.error('Error processing sprint document:', error);
            alert('Error processing sprint document! Please check the console for details.');
        } finally {
            // Reset button state
            e.target.textContent = originalButtonText;
            e.target.disabled = false;
        }
    };

    const handleExportToJira = async (ticketId) => {
        try {
            const response = await apiRequest(`http://localhost:5000/api/tickets/${ticketId}/export-jira`, {
                method: 'POST'
            });

            if (response.ok) {
                alert('Ticket exported to Jira successfully!');
                // Refresh tickets to get updated Jira ID
                const ticketsResponse = await apiRequest('http://localhost:5000/api/tickets');
                const ticketsData = await ticketsResponse.json();
                const uniqueTickets = removeDuplicateTickets(ticketsData);
                setTickets(uniqueTickets);
            } else {
                alert('Error exporting ticket to Jira!');
            }
        } catch (error) {
            console.error('Error exporting ticket to Jira:', error);
            alert('Error exporting ticket to Jira!');
        }
    };

    const handleOptimizeWorkload = async () => {
        try {
            const response = await apiRequest('http://localhost:5000/api/system/optimize-workload', {
                method: 'POST'
            });

            if (response.ok) {
                const result = await response.json();
                alert(`Workload optimized! ${result.assignments.length} tickets reassigned.`);
                // Refresh data
                fetchInitialData();
            } else {
                alert('Error optimizing workload!');
            }
        } catch (error) {
            console.error('Error optimizing workload:', error);
            alert('Error optimizing workload!');
        }
    };

    const handleBalanceWorkload = async () => {
        try {
            const response = await apiRequest('http://localhost:5000/api/system/balance-workload');

            if (response.ok) {
                const balanceInfo = await response.json();

                let message = `Average Utilization: ${(balanceInfo.average_utilization * 100).toFixed(1)}%\n\n`;
                message += "Workload Distribution:\n";

                balanceInfo.workload_distribution.forEach(dev => {
                    message += `${dev.developer_name}: ${(dev.utilization * 100).toFixed(1)}% utilization\n`;
                });

                if (balanceInfo.suggestions.length > 0) {
                    message += "\nRebalancing Suggestions:\n";
                    balanceInfo.suggestions.forEach(suggestion => {
                        message += `- Transfer ${suggestion.transfer_hours.toFixed(1)}h from ${suggestion.from_developer} to ${suggestion.to_developer}\n`;
                    });
                }

                alert(message);
            } else {
                alert('Error analyzing workload balance!');
            }
        } catch (error) {
            console.error('Error analyzing workload balance:', error);
            alert('Error analyzing workload balance!');
        }
    };

    const handleGenerateProgressReport = async () => {
        try {
            const response = await apiRequest('http://localhost:5000/api/system/progress-report');

            if (response.ok) {
                const report = await response.json();

                let reportText = `Progress Report generated on ${new Date(report.generated_at).toLocaleString()}\n\n`;
                reportText += `Summary:\n`;
                reportText += `- Total Tickets: ${report.summary.total_tickets}\n`;
                reportText += `- Completed: ${report.summary.completed_tickets} (${(report.summary.completion_rate * 100).toFixed(1)}%)\n`;
                reportText += `- In Progress: ${report.summary.in_progress_tickets}\n`;
                reportText += `- Backlog: ${report.summary.backlog_tickets}\n\n`;

                if (report.bottlenecks.length > 0) {
                    reportText += `Bottlenecks:\n`;
                    report.bottlenecks.forEach(bottleneck => {
                        if (bottleneck.type === 'developer') {
                            reportText += `- ${bottleneck.developer_name}: ${(bottleneck.utilization * 100).toFixed(1)}% utilization (${bottleneck.severity} severity)\n`;
                        } else {
                            reportText += `- Task "${bottleneck.ticket_title}": ${bottleneck.dependencies} dependencies\n`;
                        }
                    });
                    reportText += '\n';
                }

                if (report.slow_tasks.length > 0) {
                    reportText += `Slow Tasks:\n`;
                    report.slow_tasks.forEach(task => {
                        reportText += `- "${task.ticket_title}": ${task.overrun_ratio.toFixed(1)}x over estimate\n`;
                    });
                    reportText += '\n';
                }

                if (report.insights.length > 0) {
                    reportText += `Insights:\n`;
                    report.insights.forEach(insight => {
                        reportText += `- ${insight.message}\n`;
                    });
                }

                // Create a downloadable file
                const blob = new Blob([reportText], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `progress_report_${new Date().toISOString().split('T')[0]}.txt`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } else {
                alert('Error generating progress report!');
            }
        } catch (error) {
            console.error('Error generating progress report:', error);
            alert('Error generating progress report!');
        }
    };

    const handleAdjustPriorities = async () => {
        try {
            const response = await apiRequest('http://localhost:5000/api/system/adjust-priorities', {
                method: 'POST'
            });

            if (response.ok) {
                const result = await response.json();

                if (result.adjustments.length > 0) {
                    let message = `Priority adjustments made:\n\n`;
                    result.adjustments.forEach(adj => {
                        message += `- Ticket ${adj.ticket_id}: ${adj.old_priority} → ${adj.new_priority} (${adj.reason})\n`;
                    });
                    alert(message);
                } else {
                    alert("No priority adjustments needed at this time.");
                }

                // Refresh data
                fetchInitialData();
            } else {
                alert('Error adjusting priorities!');
            }
        } catch (error) {
            console.error('Error adjusting priorities:', error);
            alert('Error adjusting priorities!');
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'backlog': return '#ffc107'; // Yellow
            case 'in_progress': return '#007bff'; // Blue
            case 'completed': return '#28a745'; // Green
            default: return '#6c757d'; // Gray
        }
    };

    const getPriorityColor = (priority) => {
        switch (priority) {
            case 'critical': return '#dc3545'; // Red
            case 'high': return '#fd7e14'; // Orange
            case 'medium': return '#ffc107'; // Yellow
            case 'low': return '#28a745'; // Green
            default: return '#6c757d'; // Gray
        }
    };

    // Navigation buttons
    const renderNavigation = () => (
        <div className="navigation-panel">
            <h2>Smart Sprint Menu</h2>
            <div className="nav-buttons">
                <button
                    className={`nav-btn ${activeView === 'dashboard' ? 'active' : ''}`}
                    onClick={() => setActiveView('dashboard')}
                >
                    Dashboard
                </button>
                <button
                    className={`nav-btn ${activeView === 'tickets' ? 'active' : ''}`}
                    onClick={() => setActiveView('tickets')}
                >
                    1. View all tickets
                </button>
                <button
                    className={`nav-btn ${activeView === 'developers' ? 'active' : ''}`}
                    onClick={() => setActiveView('developers')}
                >
                    2. View all developers
                </button>
                <button
                    className={`nav-btn ${activeView === 'create' ? 'active' : ''}`}
                    onClick={() => setActiveView('create')}
                >
                    3. Process new feature story
                </button>
                <button
                    className={`nav-btn ${activeView === 'assign' ? 'active' : ''}`}
                    onClick={() => {
                        setActiveView('assign');
                        setSelectedTicket(null);
                        setRecommendations([]);
                        setTimeline(null);
                    }}
                >
                    4. Get recommendations, estimate timeline, and assign developer
                </button>
                <button
                    className={`nav-btn ${activeView === 'complete' ? 'active' : ''}`}
                    onClick={() => {
                        setActiveView('complete');
                        setSelectedTicket(null);
                    }}
                >
                    5. Complete ticket
                </button>
                <button
                    className={`nav-btn ${activeView === 'status' ? 'active' : ''}`}
                    onClick={() => setActiveView('status')}
                >
                    6. View system status
                </button>
                <button
                    className={`nav-btn ${activeView === 'performance' ? 'active' : ''}`}
                    onClick={() => {
                        setActiveView('performance');
                        setSelectedDeveloper(null);
                        setDeveloperPerformance(null);
                    }}
                >
                    7. View developer performance
                </button>
                <button
                    className={`nav-btn ${activeView === 'document' ? 'active' : ''}`}
                    onClick={() => setActiveView('document')}
                >
                    8. Process document
                </button>
                <button
                    className={`nav-btn ${activeView === 'sprint' ? 'active' : ''}`}
                    onClick={() => setActiveView('sprint')}
                >
                    9. Process sprint document with user stories
                </button>
                <button
                    className={`nav-btn ${activeView === 'save' ? 'active' : ''}`}
                    onClick={() => setActiveView('save')}
                >
                    10. Save data manually
                </button>
                <button
                    className="nav-btn exit-btn"
                    onClick={() => {
                        if (window.confirm('Are you sure you want to exit?')) {
                            alert('Thank you for using Smart Sprint!');
                            window.close();
                        }
                    }}
                >
                    11. Exit
                </button>
            </div>
        </div>
    );

    // Login form
    const renderLoginForm = () => (
        <div className="login-form">
            <h2>Login to Smart Sprint</h2>
            <form onSubmit={(e) => {
                e.preventDefault();
                const username = e.target.username.value;
                const password = e.target.password.value;
                login(username, password);
            }}>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" name="username" required />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" required />
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
            <p>Default credentials: admin/admin123 or user/user123</p>
        </div>
    );

    // Dashboard View
    const renderDashboardView = () => (
        <Dashboard />
    );

    // Tickets View
    const renderTicketsView = () => (
        <div className="tickets-view">
            <h2>All Tickets</h2>
            <div className="tickets-table">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Status</th>
                            <th>Priority</th>
                            <th>Assigned To</th>
                            <th>Estimated Hours</th>
                            <th>Jira ID</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tickets.map(ticket => {
                            const assignedDeveloper = developers.find(d => d.id === ticket.assigned_to);
                            return (
                                <tr key={ticket.id}>
                                    <td>{ticket.id}</td>
                                    <td>{ticket.title}</td>
                                    <td>
                                        <span className="status-badge" style={{ backgroundColor: getStatusColor(ticket.status) }}>
                                            {ticket.status.replace('_', ' ')}
                                        </span>
                                    </td>
                                    <td>
                                        <span className="priority-badge" style={{ backgroundColor: getPriorityColor(ticket.priority) }}>
                                            {ticket.priority}
                                        </span>
                                    </td>
                                    <td>{assignedDeveloper ? assignedDeveloper.name : 'Unassigned'}</td>
                                    <td>{Math.ceil(ticket.estimated_hours)}h</td>
                                    <td>{ticket.jira_id || '-'}</td>
                                    <td>
                                        <div className="action-buttons">
                                            <button className="btn btn-sm" onClick={() => {
                                                setSelectedTicket(ticket);
                                                setActiveView('viewTicket');
                                            }}>View</button>
                                            {ticket.status === 'backlog' && (
                                                <button
                                                    className="btn btn-sm btn-primary"
                                                    onClick={() => {
                                                        setSelectedTicket(ticket);
                                                        setActiveView('assign');
                                                    }}
                                                >
                                                    Assign
                                                </button>
                                            )}
                                            {ticket.status === 'in_progress' && (
                                                <button
                                                    className="btn btn-sm btn-success"
                                                    onClick={() => {
                                                        setSelectedTicket(ticket);
                                                        setActiveView('complete');
                                                    }}
                                                >
                                                    Complete
                                                </button>
                                            )}
                                            <button
                                                className="btn btn-sm"
                                                onClick={() => handleExportToJira(ticket.id)}
                                                disabled={ticket.jira_id}
                                            >
                                                {ticket.jira_id ? 'Exported' : 'Export to Jira'}
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );

    // View Ticket Detail View
    const renderViewTicketView = () => {
        if (!selectedTicket) {
            return (
                <div className="view-ticket-view">
                    <h2>View Ticket</h2>
                    <p>No ticket selected. Please select a ticket to view.</p>
                    <button className="btn btn-primary" onClick={() => setActiveView('tickets')}>
                        Back to Tickets
                    </button>
                </div>
            );
        }

        const assignedDeveloper = developers.find(d => d.id === selectedTicket.assigned_to);
        return (
            <div className="view-ticket-view">
                <h2>View Ticket</h2>
                <div className="ticket-details">
                    <div className="ticket-header">
                        <h3>{selectedTicket.title}</h3>
                        <div className="ticket-meta">
                            <span className="ticket-id">ID: {selectedTicket.id}</span>
                            <span className="status-badge" style={{ backgroundColor: getStatusColor(selectedTicket.status) }}>
                                {selectedTicket.status.replace('_', ' ')}
                            </span>
                            <span className="priority-badge" style={{ backgroundColor: getPriorityColor(selectedTicket.priority) }}>
                                {selectedTicket.priority}
                            </span>
                        </div>
                    </div>
                    <div className="ticket-info">
                        <div className="info-section">
                            <h4>Description</h4>
                            <p>{selectedTicket.description}</p>
                        </div>
                        <div className="info-section">
                            <h4>Details</h4>
                            <div className="info-grid">
                                <div className="info-item">
                                    <span className="info-label">Estimated Hours:</span>
                                    <span className="info-value">{Math.ceil(selectedTicket.estimated_hours)}h</span>
                                </div>
                                <div className="info-item">
                                    <span className="info-label">Complexity:</span>
                                    <span className="info-value">{selectedTicket.complexity}</span>
                                </div>
                                <div className="info-item">
                                    <span className="info-label">Assigned To:</span>
                                    <span className="info-value">{assignedDeveloper ? assignedDeveloper.name : 'Unassigned'}</span>
                                </div>
                            </div>
                        </div>
                        <div className="info-section">
                            <h4>Tasks</h4>
                            <ul className="task-list">
                                {selectedTicket.tasks.map((task, index) => (
                                    <li key={index}>{task}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                    <div className="action-buttons">
                        <button
                            className="btn btn-secondary"
                            onClick={() => setActiveView('tickets')}
                        >
                            Back to Tickets
                        </button>
                        <button
                            className="btn btn-primary"
                            onClick={() => setActiveView('dashboard')}
                        >
                            Back to Dashboard
                        </button>
                        {selectedTicket.status === 'backlog' && (
                            <button
                                className="btn btn-primary"
                                onClick={() => {
                                    setActiveView('assign');
                                }}
                            >
                                Assign Ticket
                            </button>
                        )}
                        {selectedTicket.status === 'in_progress' && (
                            <button
                                className="btn btn-success"
                                onClick={() => {
                                    setActiveView('complete');
                                }}
                            >
                                Complete Ticket
                            </button>
                        )}
                    </div>
                </div>
            </div>
        );
    };

    // Developers View
    const renderDevelopersView = () => (
        <div className="developers-view">
            <h2>All Developers</h2>
            <div className="developers-grid">
                {developers.map(developer => (
                    <div key={developer.id} className="developer-card">
                        <div className="developer-header">
                            <div className="developer-avatar">
                                {developer.name.split(' ').map(n => n[0]).join('')}
                            </div>
                            <div>
                                <h3>{developer.name}</h3>
                                <span className="developer-level">Level {developer.experience_level}</span>
                            </div>
                        </div>
                        <div className="developer-stats">
                            <div className="stat">
                                <span className="stat-label">Availability</span>
                                <span className="stat-value">{developer.availability}h</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">Current Workload</span>
                                <span className="stat-value">{developer.current_workload}h</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">Utilization</span>
                                <span className="stat-value">
                                    {(developer.current_workload / developer.availability * 100).toFixed(1)}%
                                </span>
                            </div>
                        </div>
                        <div className="developer-skills">
                            <h4>Skills</h4>
                            <div className="skills-list">
                                {developer.skills.map((skill, index) => (
                                    <span key={index} className="skill-tag">{skill}</span>
                                ))}
                            </div>
                        </div>
                        <button
                            className="btn btn-primary"
                            onClick={() => {
                                setSelectedDeveloper(developer);
                                setDeveloperPerformance(null);
                                setActiveView('performance');
                            }}
                        >
                            View Performance
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );

    // Create Ticket View
    const renderCreateTicketView = () => (
        <div className="create-ticket-view">
            <h2>Process New Feature Story</h2>
            <form className="create-ticket-form" onSubmit={handleCreateTicket}>
                <div className="form-group">
                    <label htmlFor="title">Title</label>
                    <input
                        type="text"
                        id="title"
                        value={newTicket.title}
                        onChange={(e) => setNewTicket({ ...newTicket, title: e.target.value })}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="description">Description</label>
                    <textarea
                        id="description"
                        value={newTicket.description}
                        onChange={(e) => setNewTicket({ ...newTicket, description: e.target.value })}
                        rows="4"
                        required
                    ></textarea>
                </div>
                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="priority">Priority</label>
                        <select
                            id="priority"
                            value={newTicket.priority}
                            onChange={(e) => setNewTicket({ ...newTicket, priority: e.target.value })}
                        >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="critical">Critical</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="estimated_hours">Estimated Hours</label>
                        <input
                            type="number"
                            id="estimated_hours"
                            value={newTicket.estimated_hours}
                            onChange={(e) => setNewTicket({ ...newTicket, estimated_hours: parseInt(e.target.value) })}
                            min="1"
                            required
                        />
                    </div>
                </div>
                <div className="form-actions">
                    <button type="submit" className="btn btn-primary">Create Ticket</button>
                    <button type="button" className="btn btn-secondary" onClick={() => setActiveView('dashboard')}>Cancel</button>
                </div>
            </form>
        </div>
    );

    // Assign Ticket View
    const renderAssignTicketView = () => (
        <div className="assign-ticket-view">
            <h2>Get Recommendations, Estimate Timeline, and Assign Developer</h2>
            {!selectedTicket ? (
                <div className="ticket-selection">
                    <h3>Select a ticket to assign:</h3>
                    <div className="ticket-list">
                        {tickets.filter(t => t.status === 'backlog').map(ticket => (
                            <div key={ticket.id} className="ticket-select-item" onClick={() => setSelectedTicket(ticket)}>
                                <span className="ticket-id">{ticket.id}</span>
                                <span className="ticket-title">{ticket.title}</span>
                                <span className="ticket-priority" style={{ backgroundColor: getPriorityColor(ticket.priority) }}>
                                    {ticket.priority}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            ) : (
                <div className="assign-ticket-content">
                    <div className="ticket-details">
                        <h3>Ticket Details</h3>
                        <p><strong>ID:</strong> {selectedTicket.id}</p>
                        <p><strong>Title:</strong> {selectedTicket.title}</p>
                        <p><strong>Description:</strong> {selectedTicket.description}</p>
                        <p><strong>Priority:</strong> {selectedTicket.priority}</p>
                        <p><strong>Estimated Hours:</strong> {Math.ceil(selectedTicket.estimated_hours)}h</p>
                        <p><strong>Complexity:</strong> {selectedTicket.complexity}</p>
                        <div>
                            <strong>Tasks:</strong>
                            <ul>
                                {selectedTicket.tasks.map((task, index) => (
                                    <li key={index}>{task}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                    <div className="recommendation-section">
                        <div className="action-buttons">
                            <button
                                className="btn btn-primary"
                                onClick={() => handleGetRecommendations(selectedTicket.id)}
                                disabled={recommendations.length > 0}
                            >
                                Get Recommendations
                            </button>
                            <button
                                className="btn btn-secondary"
                                onClick={() => {
                                    setSelectedTicket(null);
                                    setRecommendations([]);
                                    setTimeline(null);
                                }}
                            >
                                Back
                            </button>
                        </div>
                        {recommendations.length > 0 && (
                            <div className="recommendations">
                                <h3>Recommended Developers</h3>
                                <div className="developers-list">
                                    {recommendations.map((rec, index) => (
                                        <div key={index} className="developer-option">
                                            <div className="developer-info">
                                                <div className="developer-avatar">
                                                    {rec.developer_name.split(' ').map(n => n[0]).join('')}
                                                </div>
                                                <div>
                                                    <h4>{rec.developer_name}</h4>
                                                    <div className="developer-match">
                                                        <span>Match Score: {rec.match_score.toFixed(2)}</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <button
                                                className="btn btn-success"
                                                onClick={() => {
                                                    handleAssignTicket(selectedTicket.id, rec.developer_id);
                                                    setSelectedTicket(null);
                                                    setRecommendations([]);
                                                    setTimeline(null);
                                                }}
                                            >
                                                Assign
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                        {timeline && (
                            <div className="timeline-estimate">
                                <h3>Timeline Estimate</h3>
                                <p><strong>Estimated Hours:</strong> {timeline.estimated_hours}h</p>
                                <p><strong>Mean Duration:</strong> {timeline.mean_duration}h</p>
                                <p><strong>Risk Level:</strong> {timeline.risk_level}</p>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );

    // Complete Ticket View
    const renderCompleteTicketView = () => (
        <div className="complete-ticket-view">
            <h2>Complete Ticket</h2>
            {!selectedTicket ? (
                <div className="ticket-selection">
                    <h3>Select a ticket to complete:</h3>
                    <div className="ticket-list">
                        {tickets.filter(t => t.status === 'in_progress').map(ticket => (
                            <div key={ticket.id} className="ticket-select-item" onClick={() => setSelectedTicket(ticket)}>
                                <span className="ticket-id">{ticket.id}</span>
                                <span className="ticket-title">{ticket.title}</span>
                                <span className="ticket-priority" style={{ backgroundColor: getPriorityColor(ticket.priority) }}>
                                    {ticket.priority}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            ) : (
                <div className="complete-ticket-content">
                    <div className="ticket-details">
                        <h3>Ticket Details</h3>
                        <p><strong>ID:</strong> {selectedTicket.id}</p>
                        <p><strong>Title:</strong> {selectedTicket.title}</p>
                        <p><strong>Description:</strong> {selectedTicket.description}</p>
                        <p><strong>Priority:</strong> {selectedTicket.priority}</p>
                        <p><strong>Estimated Hours:</strong> {Math.ceil(selectedTicket.estimated_hours)}h</p>
                    </div>
                    <div className="completion-form">
                        <h3>Completion Details</h3>
                        <div className="form-group">
                            <label htmlFor="completion_time">Actual Completion Time (hours)</label>
                            <input
                                type="number"
                                id="completion_time"
                                value={completeTicketData.completion_time}
                                onChange={(e) => setCompleteTicketData({ ...completeTicketData, completion_time: parseFloat(e.target.value) })}
                                min="0.1"
                                step="0.1"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="revisions">Number of Revisions</label>
                            <input
                                type="number"
                                id="revisions"
                                value={completeTicketData.revisions}
                                onChange={(e) => setCompleteTicketData({ ...completeTicketData, revisions: parseInt(e.target.value) })}
                                min="0"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="sentiment_score">Sentiment Score (0-1)</label>
                            <input
                                type="number"
                                id="sentiment_score"
                                value={completeTicketData.sentiment_score}
                                onChange={(e) => setCompleteTicketData({ ...completeTicketData, sentiment_score: parseFloat(e.target.value) })}
                                min="0"
                                max="1"
                                step="0.01"
                                required
                            />
                        </div>
                        <div className="form-actions">
                            <button
                                className="btn btn-success"
                                onClick={() => handleCompleteTicket(selectedTicket.id)}
                            >
                                Complete Ticket
                            </button>
                            <button
                                className="btn btn-secondary"
                                onClick={() => {
                                    setSelectedTicket(null);
                                }}
                            >
                                Back
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );

    // System Status View
    const renderSystemStatusView = () => (
        <div className="system-status-view">
            <h2>System Status</h2>
            <div className="status-cards">
                <div className="status-card">
                    <h3>Total Tickets</h3>
                    <div className="status-value">{systemStatus.total_tickets}</div>
                </div>
                <div className="status-card">
                    <h3>Completed Tickets</h3>
                    <div className="status-value">{systemStatus.completed_tickets}</div>
                </div>
                <div className="status-card">
                    <h3>In Progress Tickets</h3>
                    <div className="status-value">{systemStatus.in_progress_tickets}</div>
                </div>
                <div className="status-card">
                    <h3>Backlog Tickets</h3>
                    <div className="status-value">{systemStatus.backlog_tickets}</div>
                </div>
                <div className="status-card">
                    <h3>Total Workload</h3>
                    <div className="status-value">{systemStatus.total_workload} hours</div>
                </div>
                <div className="status-card">
                    <h3>Total Availability</h3>
                    <div className="status-value">{systemStatus.total_availability} hours</div>
                </div>
                <div className="status-card">
                    <h3>Utilization Rate</h3>
                    <div className="status-value">{systemStatus.utilization_rate?.toFixed(1)}%</div>
                </div>
            </div>
            <div className="action-buttons">
                <button
                    className="btn btn-primary"
                    onClick={handleOptimizeWorkload}
                >
                    Optimize Workload
                </button>
                <button
                    className="btn btn-secondary"
                    onClick={handleBalanceWorkload}
                >
                    Balance Workload Analysis
                </button>
                <button
                    className="btn btn-primary"
                    onClick={handleGenerateProgressReport}
                >
                    Generate Progress Report
                </button>
                <button
                    className="btn btn-secondary"
                    onClick={handleAdjustPriorities}
                >
                    Adjust Priorities Dynamically
                </button>
            </div>
        </div>
    );

    // Developer Performance View
    const renderDeveloperPerformanceView = () => (
        <div className="developer-performance-view">
            <h2>Developer Performance</h2>
            {!selectedDeveloper ? (
                <div className="developer-selection">
                    <h3>Select a developer:</h3>
                    <div className="developer-list">
                        {developers.map(developer => (
                            <div key={developer.id} className="developer-select-item" onClick={() => {
                                setSelectedDeveloper(developer);
                                fetchDeveloperPerformance(developer.id);
                            }}>
                                <div className="developer-avatar">
                                    {developer.name.split(' ').map(n => n[0]).join('')}
                                </div>
                                <div>
                                    <span className="developer-name">{developer.name}</span>
                                    <span className="developer-level">Level {developer.experience_level}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="action-buttons">
                        <button
                            className="btn btn-primary"
                            onClick={() => setActiveView('dashboard')}
                        >
                            Back to Dashboard
                        </button>
                    </div>
                </div>
            ) : (
                <div className="performance-details">
                    <div className="developer-header">
                        <div className="developer-avatar">
                            {selectedDeveloper.name.split(' ').map(n => n[0]).join('')}
                        </div>
                        <div>
                            <h3>{selectedDeveloper.name}</h3>
                            <span className="developer-level">Level {selectedDeveloper.experience_level}</span>
                        </div>
                    </div>
                    <div className="performance-stats">
                        <div className="performance-stat">
                            <h4>Availability</h4>
                            <p>{selectedDeveloper.availability} hours</p>
                        </div>
                        <div className="performance-stat">
                            <h4>Current Workload</h4>
                            <p>{selectedDeveloper.current_workload} hours</p>
                        </div>
                        <div className="performance-stat">
                            <h4>Utilization</h4>
                            <p>{(selectedDeveloper.current_workload / selectedDeveloper.availability * 100).toFixed(1)}%</p>
                        </div>
                        <div className="performance-stat">
                            <h4>Skills</h4>
                            <div className="skills-list">
                                {selectedDeveloper.skills.map((skill, index) => (
                                    <span key={index} className="skill-tag">{skill}</span>
                                ))}
                            </div>
                        </div>
                    </div>
                    {developerPerformance ? (
                        <div className="historical-performance">
                            <h3>Historical Performance</h3>
                            <div className="performance-metrics">
                                <div className="metric">
                                    <h4>Average Completion Time</h4>
                                    <p>{developerPerformance.average_completion_time?.toFixed(1) || 'N/A'} hours</p>
                                </div>
                                <div className="metric">
                                    <h4>Accuracy</h4>
                                    <p>{(developerPerformance.accuracy * 100)?.toFixed(1) || 'N/A'}%</p>
                                </div>
                                <div className="metric">
                                    <h4>Total Completed Tickets</h4>
                                    <p>{developerPerformance.total_completed_tickets || 'N/A'}</p>
                                </div>
                                <div className="metric">
                                    <h4>Average Sentiment</h4>
                                    <p>{(developerPerformance.average_sentiment * 100)?.toFixed(1) || 'N/A'}%</p>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="no-performance-data">
                            <p>No performance data available for this developer.</p>
                        </div>
                    )}
                    <div className="action-buttons">
                        <button
                            className="btn btn-secondary"
                            onClick={() => {
                                setSelectedDeveloper(null);
                                setDeveloperPerformance(null);
                            }}
                        >
                            Back to Developers
                        </button>
                        <button
                            className="btn btn-primary"
                            onClick={() => setActiveView('dashboard')}
                        >
                            Back to Dashboard
                        </button>
                    </div>
                </div>
            )}
        </div>
    );

    // Process Document View
    const renderProcessDocumentView = () => (
        <div className="process-document-view">
            <h2>Process Document</h2>
            <div className="document-form">
                <div className="form-group">
                    <label htmlFor="documentPath">Document Path</label>
                    <input
                        type="text"
                        id="documentPath"
                        value={documentPath}
                        onChange={(e) => setDocumentPath(e.target.value)}
                        placeholder="Enter path to document (.docx, .txt)"
                        required
                    />
                </div>
                <div className="form-actions">
                    <button
                        className="btn btn-primary"
                        onClick={handleProcessDocument}
                    >
                        Process Document
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={() => setActiveView('dashboard')}
                    >
                        Cancel
                    </button>
                </div>
            </div>
            <div className="document-info">
                <h3>About Document Processing</h3>
                <p>This feature allows you to upload a document and automatically extract tasks from it.</p>
                <p>Supported formats:</p>
                <ul>
                    <li>Word documents (.docx)</li>
                    <li>Text files (.txt)</li>
                </ul>
                <p>The system will analyze the document and create tickets for each task found.</p>
            </div>
        </div>
    );

    // Process Sprint Document View
    const renderProcessSprintDocumentView = () => (
        <div className="process-sprint-document-view">
            <h2>Process Sprint Document with User Stories</h2>
            <div className="document-form">
                <div className="form-group">
                    <label htmlFor="sprintDocumentPath">Sprint Document Path</label>
                    <input
                        type="text"
                        id="sprintDocumentPath"
                        value={sprintDocumentPath}
                        onChange={(e) => setSprintDocumentPath(e.target.value)}
                        placeholder="Example: C:\Users\shrad\source\repos\smart_sprint_framework\smart_sprint_framework\sprint_documents\SprintStory.docx"
                        required
                    />
                </div>
                <div className="form-actions">
                    <button
                        className="btn btn-primary"
                        onClick={handleProcessSprintDocument}
                    >
                        Process Sprint Document
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={() => setActiveView('dashboard')}
                    >
                        Cancel
                    </button>
                </div>
            </div>
            <div className="document-info">
                <h3>About Sprint Document Processing</h3>
                <p>This feature allows you to upload a sprint document with user stories and automatically generate tasks.</p>
                <p><strong>Required Document Format:</strong></p>
                <ul>
                    <li>Sprint Goal: "Your sprint goal here"</li>
                    <li>User Stories in format: "As a [user type], I want [action] so that [benefit]" (Story Points: X)</li>
                </ul>
                <p><strong>Example:</strong></p>
                <pre>
                    {`Sprint Goal: "Implement user authentication system"
User Stories:
"As a user, I want to register for an account so that I can access the application" (Story Points: 5)
"As a user, I want to login with my credentials so that I can access my account" (Story Points: 3)`}
                </pre>
                <p><strong>Supported formats:</strong></p>
                <ul>
                    <li>Word documents (.docx)</li>
                    <li>Text files (.txt)</li>
                </ul>
                <p>The system will analyze the document and create tickets for each user story.</p>
            </div>
        </div>
    );

    // Save Data View
    const renderSaveDataView = () => (
        <div className="save-data-view">
            <h2>Save Data Manually</h2>
            <div className="save-info">
                <p>This will manually save all current data to CSV files.</p>
                <p>This is useful for creating backups or before making significant changes.</p>
            </div>
            <div className="action-buttons">
                <button
                    className="btn btn-primary"
                    onClick={handleSaveData}
                >
                    Save Data Now
                </button>
                <button
                    className="btn btn-secondary"
                    onClick={() => setActiveView('dashboard')}
                >
                    Cancel
                </button>
            </div>
        </div>
    );

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (!isAuthenticated) {
        return (
            <div className="app">
                <header className="app-header">
                    <div className="logo">
                        <h1>Smart Sprint</h1>
                        <span>AI-Enhanced Kanban Solution</span>
                    </div>
                </header>
                <div className="main-content">
                    {renderLoginForm()}
                </div>
            </div>
        );
    }

    return (
        <div className="app">
            <header className="app-header">
                <div className="logo">
                    <h1>Smart Sprint</h1>
                    <span>AI-Enhanced Kanban Solution</span>
                </div>
                <div className="user-info">
                    <span>Welcome, {user.username} ({user.role})</span>
                    <button className="btn btn-sm" onClick={logout}>Logout</button>
                </div>
            </header>
            <div className="main-content">
                {renderNavigation()}
                <div className="content-area">
                    {activeView === 'dashboard' && renderDashboardView()}
                    {activeView === 'tickets' && renderTicketsView()}
                    {activeView === 'viewTicket' && renderViewTicketView()}
                    {activeView === 'developers' && renderDevelopersView()}
                    {activeView === 'create' && renderCreateTicketView()}
                    {activeView === 'assign' && renderAssignTicketView()}
                    {activeView === 'complete' && renderCompleteTicketView()}
                    {activeView === 'status' && renderSystemStatusView()}
                    {activeView === 'performance' && renderDeveloperPerformanceView()}
                    {activeView === 'document' && renderProcessDocumentView()}
                    {activeView === 'sprint' && renderProcessSprintDocumentView()}
                    {activeView === 'save' && renderSaveDataView()}
                </div>
            </div>
        </div>
    );
}

export default App;