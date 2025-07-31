import React, { useState, useEffect } from 'react';
import './App.css';

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/dashboard', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setDashboardData(data);
                } else {
                    alert('Error fetching dashboard data');
                }
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
                alert('Error fetching dashboard data');
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, []);

    if (loading) {
        return <div className="loading">Loading dashboard...</div>;
    }

    if (!dashboardData) {
        return <div>Error loading dashboard data</div>;
    }

    const { summary, ticket_trends, developer_performance, priority_distribution,
        complexity_analysis, workload_distribution, velocity_tracking, burndown_data } = dashboardData;

    return (
        <div className="dashboard-view">
            <h2>Project Dashboard</h2>

            {/* Summary Cards */}
            <div className="dashboard-stats">
                <div className="stat-card">
                    <h3>Total Tickets</h3>
                    <div className="stat-value">{summary.total_tickets}</div>
                </div>
                <div className="stat-card">
                    <h3>Completed</h3>
                    <div className="stat-value">{summary.completed_tickets}</div>
                </div>
                <div className="stat-card">
                    <h3>In Progress</h3>
                    <div className="stat-value">{summary.in_progress_tickets}</div>
                </div>
                <div className="stat-card">
                    <h3>Backlog</h3>
                    <div className="stat-value">{summary.backlog_tickets}</div>
                </div>
                <div className="stat-card">
                    <h3>Completion Rate</h3>
                    <div className="stat-value">{summary.completion_rate}%</div>
                </div>
                <div className="stat-card">
                    <h3>Utilization Rate</h3>
                    <div className="stat-value">{summary.utilization_rate}%</div>
                </div>
            </div>

            {/* Charts Section */}
            <div className="dashboard-charts">
                {/* Priority Distribution */}
                <div className="chart-container">
                    <h3>Priority Distribution</h3>
                    <div className="chart">
                        {priority_distribution.map(item => (
                            <div key={item.priority} className="bar-chart-item">
                                <div className="bar-label">{item.priority}</div>
                                <div
                                    className="bar"
                                    style={{
                                        width: `${item.percentage}%`,
                                        backgroundColor: getPriorityColor(item.priority)
                                    }}
                                ></div>
                                <div className="bar-value">{item.count} ({item.percentage}%)</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Complexity Analysis */}
                <div className="chart-container">
                    <h3>Complexity Analysis</h3>
                    <div className="chart">
                        {complexity_analysis.map(item => (
                            <div key={item.complexity} className="bar-chart-item">
                                <div className="bar-label">Level {item.complexity}</div>
                                <div
                                    className="bar"
                                    style={{
                                        width: `${item.percentage}%`,
                                        backgroundColor: getComplexityColor(item.complexity)
                                    }}
                                ></div>
                                <div className="bar-value">{item.count} ({item.percentage}%)</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Workload Distribution */}
                <div className="chart-container">
                    <h3>Workload Distribution</h3>
                    <div className="chart">
                        {workload_distribution.map(dev => (
                            <div key={dev.developer_id} className="workload-item">
                                <div className="developer-name">{dev.developer_name}</div>
                                <div className="workload-bar-container">
                                    <div
                                        className="workload-bar"
                                        style={{ width: `${dev.utilization}%` }}
                                    ></div>
                                </div>
                                <div className="workload-value">{dev.utilization}%</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Developer Performance */}
                <div className="chart-container">
                    <h3>Developer Performance</h3>
                    <div className="performance-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Developer</th>
                                    <th>Utilization</th>
                                    <th>Velocity</th>
                                    <th>Accuracy</th>
                                    <th>Sentiment</th>
                                    <th>Completed</th>
                                </tr>
                            </thead>
                            <tbody>
                                {developer_performance.map(dev => (
                                    <tr key={dev.developer_id}>
                                        <td>{dev.developer_name}</td>
                                        <td>{dev.utilization}%</td>
                                        <td>{dev.velocity}h</td>
                                        <td>{dev.accuracy}%</td>
                                        <td>{dev.sentiment}%</td>
                                        <td>{dev.tickets_completed}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Velocity Tracking */}
                <div className="chart-container">
                    <h3>Velocity Tracking</h3>
                    <div className="chart">
                        <div className="line-chart">
                            {velocity_tracking.map((week, index) => (
                                <div key={index} className="line-chart-point">
                                    <div className="point-label">{week.week}</div>
                                    <div className="point-container">
                                        <div
                                            className="point planned"
                                            style={{ bottom: `${week.planned_velocity}%` }}
                                            title={`Planned: ${week.planned_velocity}h`}
                                        ></div>
                                        <div
                                            className="point actual"
                                            style={{ bottom: `${week.actual_velocity}%` }}
                                            title={`Actual: ${week.actual_velocity}h`}
                                        ></div>
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

                {/* Burndown Chart */}
                <div className="chart-container">
                    <h3>Burndown Chart</h3>
                    <div className="chart">
                        <div className="burndown-chart">
                            {burndown_data.map((day, index) => (
                                <div key={index} className="burndown-day">
                                    <div className="day-label">{day.date.split('-')[2]}</div>
                                    <div className="burndown-container">
                                        <div
                                            className="burndown-ideal"
                                            style={{ height: `${day.ideal_remaining}%` }}
                                        ></div>
                                        <div
                                            className="burndown-actual"
                                            style={{ height: `${day.remaining_work}%` }}
                                        ></div>
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
            </div>
        </div>
    );
};

// Helper functions
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