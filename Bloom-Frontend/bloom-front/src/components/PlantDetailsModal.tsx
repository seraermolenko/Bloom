import { PlantInGarden } from '../types/models';
import PlantInfo from './PlantInfo';

type Props = {
  plant: Partial<PlantInGarden>;
  onClose: () => void;
  onBackToSearch: () => void;
};

export default function PlantDetailsModal({ plant, onClose, onBackToSearch }: Props) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>{plant.common_name}</h2>
        
        <PlantInfo plant={plant} />

        <div className="modal-actions">
          <button onClick={onClose} className="cancel-button">Close</button>
          <button onClick={onBackToSearch} className="confirm-button">Back to Search</button>
        </div>
      </div>
    </div>
  );
}
