import React from 'react';

const StatusPanel = ({ connectionStatus, truckCount, actionCount }) => {
  const getStatusClass = (status) => {
    switch (status.toLowerCase()) {
      case 'connected': return 'status-connected';
      case 'disconnected': return 'status-disconnected';
      case 'error': return 'status-error';
      default: return '';
    }
  };

  return (
    <div className="status-panel">
      <div className="status-item">
        <div className="status-label">MQTT Connection</div>
        <div className={`status-value ${getStatusClass(connectionStatus)}`}>
          {connectionStatus}
        </div>
      </div>
      
      <div className="status-item">
        <div className="status-label">Active Trucks</div>
        <div className="status-value">
          {truckCount}
        </div>
      </div>
      
      <div className="status-item">
        <div className="status-label">RL Actions</div>
        <div className="status-value">
          {actionCount}
        </div>
      </div>
    </div>
  );
};

export default StatusPanel;
