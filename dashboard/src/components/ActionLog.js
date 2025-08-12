import React from 'react';

const ActionLog = ({ actions }) => {
  const getActionClass = (action) => {
    switch (action.toLowerCase()) {
      case 'hold': return 'action-hold';
      case 'produce': return 'action-produce';
      case 'ship': return 'action-ship';
      default: return '';
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleTimeString();
  };

  const sortedActions = [...actions].sort((a, b) => b.timestamp - a.timestamp);

  return (
    <div className="action-log">
      {actions.length === 0 ? (
        <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
          No actions recorded yet. Waiting for truck data...
        </div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Truck</th>
              <th>Action</th>
              <th>Inventory</th>
              <th>Distance</th>
            </tr>
          </thead>
          <tbody>
            {sortedActions.map((action, index) => (
              <tr key={index}>
                <td>{formatTime(action.timestamp)}</td>
                <td>Truck {action.truck_id}</td>
                <td className={getActionClass(action.action)}>
                  <strong>{action.action}</strong>
                </td>
                <td>{action.inventory} units</td>
                <td>{action.distance} km</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ActionLog;
