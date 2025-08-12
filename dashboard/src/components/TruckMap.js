import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom truck icon
const truckIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,' + btoa(`
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#007bff" width="32" height="32">
      <path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zM6 18.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm13.5-9l1.96 2.5H17V9.5h2.5zm-1.5 9c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>
    </svg>
  `),
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const TruckMap = ({ trucks }) => {
  // Default center (Los Angeles)
  const center = [34.0522, -118.2437];

  const getInventoryColor = (inventory) => {
    if (inventory > 70) return '#28a745'; // Green
    if (inventory > 30) return '#ffc107'; // Yellow
    return '#dc3545'; // Red
  };

  return (
    <MapContainer center={center} zoom={10} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      
      {Object.values(trucks).map((truck) => (
        <Marker
          key={truck.truck_id}
          position={[truck.lat, truck.lng]}
          icon={truckIcon}
        >
          <Popup>
            <div style={{ minWidth: '200px' }}>
              <h4>Truck {truck.truck_id}</h4>
              <p><strong>Location:</strong> {truck.lat.toFixed(4)}, {truck.lng.toFixed(4)}</p>
              <p>
                <strong>Inventory:</strong> 
                <span style={{ 
                  color: getInventoryColor(truck.inventory),
                  fontWeight: 'bold',
                  marginLeft: '5px'
                }}>
                  {truck.inventory} units
                </span>
              </p>
              <p><strong>Last Update:</strong> {new Date(truck.timestamp * 1000).toLocaleTimeString()}</p>
            </div>
          </Popup>
        </Marker>
      ))}
      
      {/* Warehouse marker */}
      <Marker position={center}>
        <Popup>
          <div>
            <h4>Main Warehouse</h4>
            <p>Downtown Los Angeles</p>
          </div>
        </Popup>
      </Marker>
    </MapContainer>
  );
};

export default TruckMap;
