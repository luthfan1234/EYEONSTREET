// components/MapView.tsx

'use client';

import { GoogleMap, useJsApiLoader, Marker, InfoWindow } from '@react-google-maps/api';
import React, { useState } from 'react';

interface Incident { 
  id: number; 
  cctv_id: string; 
  type: string; 
}

interface MapViewProps { 
  incidents: Incident[]; 
}

const containerStyle = {
  width: '100%',
  height: '100%',
  borderRadius: '8px',
};

const center = {
  lat: -7.563,
  lng: 110.826,
};

// Data koordinat CCTV (Format: { lat, lng })
const cctvCoordinates: { [key: string]: { lat: number, lng: number } } = {
  'Agas': { lat: -7.5658, lng: 110.8301 },
  'BalaiKota': { lat: -7.5675, lng: 110.8320 },
  'PasarGede': { lat: -7.5680, lng: 110.8335 },
  'Banjarsari': { lat: -7.5600, lng: 110.8245 },
  'Balapan01': { lat: -7.5585, lng: 110.8390 },
};

const MapView: React.FC<MapViewProps> = ({ incidents }) => {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: process.env.NEXT_PUBLIC_Maps_API_KEY!
  });

  const [activeMarker, setActiveMarker] = useState<number | null>(null);

  const handleMarkerClick = (markerId: number) => {
    setActiveMarker(markerId);
  };

  if (!isLoaded) {
    return <div>Memuat Peta Google Maps...</div>;
  }

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={14}
    >
      {incidents.map((incident) => {
        const coords = cctvCoordinates[incident.cctv_id];
        if (coords) {
          return (
            <Marker
              key={incident.id}
              position={coords}
              onClick={() => handleMarkerClick(incident.id)}
              icon={{
                url: incident.type === 'accident'
                  ? 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
                  : 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
              }}
            >
              {activeMarker === incident.id && (
                <InfoWindow onCloseClick={() => setActiveMarker(null)}>
                  <div>
                    <h4>{incident.cctv_id}</h4>
                    <p>Tipe: {incident.type}</p>
                  </div>
                </InfoWindow>
              )}
            </Marker>
          );
        }
        return null;
      })}
    </GoogleMap>
  );
};

export default MapView;