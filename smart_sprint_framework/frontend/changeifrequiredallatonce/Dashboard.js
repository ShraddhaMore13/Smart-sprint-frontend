import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:5001';

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('Authentication token not found. Please login again.');
                    setLoading(false);
                    return;
                }
                const response = await fetch(`${API_BASE_URL}/api/dashboard`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    setDashboardData(data);
                } else {
                    const errorText = await response.text();
                    setError(`Error ${response.status}: ${errorText || 'Failed to fetch dashboard data'}`);
                }
            } catch (error) {
                setError(`Network error: ${error.message || 'Failed to connect to server'}`);
            } finally {
                setLoading(false);
            }
        };
        fetchDashboardData();
    }, []);

    if (loading) {
        return <div className="loading">Loading dashboard...</div>;
    }

    if (error) {
        return (
            <div className="error-container">
                <h3>Error Loading Dashboard</h3>
                <p>{error}</p>
                <p>Please check:</p>
                <ul>
                    <li>Your Flask backend is running on port 5001</li>
                    <li>You are logged in</li>
                    <li>The server is accessible</li>
                </ul>
            </div>
        );
    }

    if (!dashboardData) {
        return <div>No dashboard data available</div>;
    }

    if (!dashboardData.summary) {
        return (
            <div className="error-container">
                <h3>Invalid Dashboard Data</h3>
                <p>The dashboard data is missing the summary object.</p>
                <pre>{JSON.stringify(dashboardData, null, 2)}</pre>
            </div>
        );
    }

    const { summary, developer_performance, priority_distribution,
        complexity_analysis, workload_distribution, velocity_tracking, burndown_data } = dashboardData;

    return (
        <div className="dashboard-view">
            <h2>Project Dashboard</h2>
            <div className="dashboard-stats">
                <div className="stat-card">
                    <h3>Total Tickets</h3>
                    <div className="stat-value">{summary.total_tickets || 0}</div>
                </div>
                <div className="stat-card">
                    <h3>Completed</h3>
                    <div className="stat-value">{summary.completed_tickets || 0}</div>
                </div>
                <div className="stat-card">
                    <h3>In Progress</h3>
                    <div className="stat-value">{summary.in_progress_tickets || 0}</div>
                </div>
                <div className="stat-card">
                    <h3>Backlog</h3>
                    <div className="stat-value">{summary.backlog_tickets || 0}</div>
                </div>
                <div className="stat-card">
                    <h3>Completion Rate</h3>
                    <div className="stat-value">{summary.completion_rate || 0}%</div>
                </div>
                <div className="stat-card">
                    <h3>Utilization Rate</h3>
                    <div className="stat-value">{summary.utilization_rate || 0}%</div>
                </div>
            </div>
            <div className="dashboard-charts">
                {priority_distribution && priority_distribution.length > 0 && (
                    <div className="chart-container">
                        <h3>Priority Distribution</h3>
                        <div className="chart">
                            {priority_distribution.map(item => (
                                <div key={item.priority} className="bar-chart-item">
                                    <div className="bar-label">{item.priority}</div>
                                    <div className="bar" style={{ width: `${item.percentage}%`, backgroundColor: getPriorityColor(item.priority) }}></div>
                                    <div className="bar-value">{item.count} ({item.percentage}%)</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                {complexity_analysis && complexity_analysis.length > 0 && (
                    <div className="chart-container">
                        <h3>Complexity Analysis</h3>
                        <div className="chart">
                            {complexity_analysis.map(item => (
                                <div key={item.complexity} className="bar-chart-item">
                                    <div className="bar-label">Level {item.complexity}</div>
                                    <div className="bar" style={{ width: `${item.percentage}%`, backgroundColor: getComplexityColor(item.complexity) }}></div>
                                    <div className="bar-value">{item.count} ({item.percentage}%)</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                {workload_distribution && workload_distribution.length > 0 && (
                    <div className="chart-container">
                        <h3>Workload Distribution</h3>
                        <div className="chart">
                            {workload_distribution.map(dev => (
                                <div key={dev.developer_id} className="workload-item">
                                    <div className="developer-name">{dev.developer_name}</div>
                                    <div className="workload-bar-container">
                                        <div className="workload-bar" style={{ width: `${dev.utilization}%` }}></div>
                                    </div>
                                    <div className="workload-value">{dev.utilization}%</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                {developer_performance && developer_performance.length > 0 && (
                    <div className="chart-container">
                        <h3>Developer Performance</h3>
                        <div className="performance-table">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Developer</th>
                                        <th>Availability</th>
                                        <th>Current Workload</th>
                                        <th>Utilization</th>
                                        <th>Velocity</th>
                                        <th>Accuracy</th>
                                        <th>Sentiment</th>
                                        <th>Completed</th>
                                        <th>Skills</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {developer_performance.map(dev => (
                                        <tr key={dev.developer_id}>
                                            <td>{dev.developer_name}</td>
                                            <td>{dev.availability}h</td>
                                            <td>{dev.current_workload}h</td>
                                            <td>{dev.utilization}%</td>
                                            <td>{dev.velocity}h</td>
                                            <td>{dev.accuracy}%</td>
                                            <td>{dev.sentiment}%</td>
                                            <td>{dev.tickets_completed}</td>
                                            <td>
                                                <div className="skills-list">
                                                    {Array.isArray(dev.skills) ? dev.skills.map((skill, index) => (
                                                        <span key={index} className="skill-tag">{skill}</span>
                                                    )) : <span className="skill-tag">{dev.skills}</span>}
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
                {velocity_tracking && velocity_tracking.length > 0 && (
                    <div className="chart-container">
                        <h3>Velocity Tracking</h3>
                        <div className="chart">
                            <div className="line-chart">
                                {velocity_tracking.map((week, index) => (
                                    <div key={index} className="line-chart-point">
                                        <div className="point-label">{week.week}</div>
                                        <div className="point-container">
                                            <div className="point planned" style={{ bottom: `${Math.min(100, week.planned_velocity / 50 * 100)}%` }} title={`Planned: ${week.planned_velocity}h`}></div>
                                            <div className="point actual" style={{ bottom: `${Math.min(100, week.actual_velocity / 50 * 100)}%` }} title={`Actual: ${week.actual_velocity}h`}></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <div className="chart-legend">
                                <div className="legend-item">
                                    <div className="legend-color planned"></div>
                                    <div>Planned Velocity</div>
                                </div>
                                <div className="legend-item">
                                    <div className="legend-color actual"></div>
                                    <div>Actual Velocity</div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
                {burndown_data && burndown_data.length > 0 && (
                    <div className="chart-container">
                        <h3>Burndown Chart</h3>
                        <div className="chart">
                            <div className="burndown-chart">
                                {burndown_data.map((day, index) => (
                                    <div key={index} className="burndown-day">
                                        <div className="day-label">{day.date.split('-')[2]}</div>
                                        <div className="burndown-container">
                                            <div className="burndown-ideal" style={{ height: `${Math.min(100, day.ideal_remaining / 100 * 100)}%` }}></div>
                                            <div className="burndown-actual" style={{ height: `${Math.min(100, day.remaining_work / 100 * 100)}%` }}></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <div className="chart-legend">
                                <div className="legend-item">
                                    <div className="legend-color ideal"></div>
                                    <div>Ideal Burndown</div>
                                </div>
                                <div className="legend-item">
                                    <div className="legend-color actual"></div>
                                    <div>Actual Burndown</div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

function getPriorityColor(priority) {
    switch (priority) {
        case 'critical': return '#dc3545';
        case 'high': return '#fd7e14';
        case 'medium': return '#ffc107';
        case 'low': return '#28a745';
        default: return '#6c757d';
    }
}

function getComplexityColor(complexity) {
    switch (complexity) {
        case 1: return '#28a745';
        case 2: return '#17a2b8';
        case 3: return '#ffc107';
        case 4: return '#fd7e14';
        case 5: return '#dc3545';
        default: return '#6c757d';
    }
}

export default Dashboard;