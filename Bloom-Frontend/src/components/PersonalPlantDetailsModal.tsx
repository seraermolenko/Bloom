import { useEffect, useState } from 'react';
import { PlantInGarden } from '../types/models';
import PlantInfo from './PlantInfo';
import StatusChartModal from './StatusChartModal'
// import WaterChartModal from './WaterChartModal'

type Props = {
  personalPlant: PlantInGarden;
  onClose: () => void;
  onDelete: () => void;
};


export default function PersonalPlantDetailsModal({ personalPlant, onClose, onDelete }: Props) {
  const [showMore, setShowMore] = useState(false);
  const [showStatusChart, setShowStatusChart] = useState(false);
  const [showWaterChart, setShowWaterChart] = useState(false);
  const [status, setStatus] = useState(personalPlant.status);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/garden/${personalPlant.garden_id}/`); 

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.updated_plant.sensor_id === personalPlant.sensor_id) {
        console.log('Received update via WebSocket:', data);
        setStatus(data.updated_plant.status); 
      }
    };

    ws.onerror = (err) => {
      console.error('WebSocket error:', err);
    };

    return () => ws.close();
  }, [personalPlant.sensor_id, personalPlant.garden_id]);


  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>{personalPlant.custom_name || personalPlant.common_name}</h2>
        <div className="plant-details">
          <p><strong>Sensor ID:</strong> {personalPlant.sensor_id || 'None'}</p>
          <p><strong>Common Name:</strong> {personalPlant.common_name}</p>
          <p><strong>Scientific Name:</strong> {personalPlant.scientific_name}</p>
          {personalPlant.sensor_id !== 0 && ( <p><strong>Status:</strong> {status || 'No status'}</p>)}
          <p><strong>Auto Watering:</strong> {personalPlant.auto_watering ? 'On' : 'Off'}</p>
          <p><strong>Last Watered:</strong> {personalPlant.last_watered ? new Date(personalPlant.last_watered).toLocaleString() : 'Not watered yet'}</p>
          {personalPlant.sensor_id !== 0 && (
          <p
          onClick={() => setShowStatusChart(true)}
          className="history-link"
        >
          View Status History
        </p>
        )}
        {personalPlant.sensor_id !== 0 && personalPlant.auto_watering && (
          <p
          onClick={() => setShowWaterChart(true)}
          className="history-link"
        >
          View Watering History
        </p>
        )}
        </div>

        

        <button 
          onClick={() => setShowMore(prev => !prev)} 
          className="toggle-more-button"
        >
          {showMore ? 'Hide Details' : 'More Info'}
        </button>

        {showMore && <PlantInfo plant={personalPlant} />}

        <div className="modal-actions">
          <button onClick={onDelete} className="delete-plant-button">
            Delete Plant
          </button>
          <button onClick={onClose} className="cancel-button">
            Close
          </button>
        </div>

        {showStatusChart && (
          <StatusChartModal
            personalPlant={personalPlant}
            onClose={() => setShowStatusChart(false)}
          />
        )}
        {showWaterChart && (
          <StatusChartModal
            personalPlant={personalPlant}
            onClose={() => setShowWaterChart(false)}
          />
        )}
      </div>
    </div>
  );
}
