import React, { useState, useEffect } from 'react';
import mqtt from 'mqtt';
import TruckMap from './components/TruckMap';
import ActionLog from './components/ActionLog';
import StatusPanel from './components/StatusPanel';
import './App.css';

function App() {
  const [trucks, setTrucks] = useState({});
  const [actions, setActions] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');
  const [mqttClient, setMqttClient] = useState(null);

  useEffect(() => {
    // Connect to MQTT broker via WebSocket
    const client = mqtt.connect('ws://localhost:9001');
    
    client.on('connect', () => {
      console.log('Connected to MQTT broker');
      setConnectionStatus('Connected');
      
      // Subscribe to truck data
      client.subscribe('trucks/+/data', (err) => {
        if (err) {
          console.error('Subscription error:', err);
        } else {
          console.log('Subscribed to truck data');
        }
      });
    });

    client.on('message', (topic, message) => {
      try {
        const data = JSON.parse(message.toString());
        const truckId = data.truck_id;
        
        setTrucks(prevTrucks => ({
          ...prevTrucks,
          [truckId]: data
        }));
      } catch (error) {
        console.error('Error parsing MQTT message:', error);
      }
    });

    client.on('error', (error) => {
      console.error('MQTT connection error:', error);
      setConnectionStatus('Error');
    });

    client.on('close', () => {
      console.log('MQTT connection closed');
      setConnectionStatus('Disconnected');
    });

    setMqttClient(client);

    // Fetch actions from edge agent API
    const fetchActions = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/actions');
        if (response.ok) {
          const actionsData = await response.json();
          setActions(actionsData);
        }
      } catch (error) {
        console.error('Error fetching actions:', error);
      }
    };

    // Fetch actions every 5 seconds
    const actionsInterval = setInterval(fetchActions, 5000);
    fetchActions(); // Initial fetch

    // Cleanup
    return () => {
      if (client) {
        client.end();
      }
      clearInterval(actionsInterval);
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Supply Chain RL Dashboard</h1>
        <StatusPanel 
          connectionStatus={connectionStatus}
          truckCount={Object.keys(trucks).length}
          actionCount={actions.length}
        />
      </header>
      
      <main className="App-main">
        <div className="dashboard-grid">
          <div className="map-container">
            <h2>Real-time Truck Locations</h2>
            <TruckMap trucks={trucks} />
          </div>
          
          <div className="actions-container">
            <h2>RL Agent Actions</h2>
            <ActionLog actions={actions} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
