type Props = {
    searchTerm: string;
    availablePlants: any[];
    onClose: () => void;
    onChangeSearch: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onSelectPlant: (plant: any) => void;
  };
  
export default function ExploreModal({
    searchTerm,
    availablePlants,
    onClose,
    onChangeSearch,
    onSelectPlant
}: Props) 
{
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h2>Explore Plants</h2>
  
          <div className="form-group">
            <label>Search Plants</label>
            <input
              type="text"
              value={searchTerm}
              onChange={onChangeSearch}
              placeholder="Search plants by common or scientific name"
            />
          </div>
  
          <div className="form-group">
            {availablePlants.map((plant) => (
              <div
                key={plant.id}
                onClick={() => onSelectPlant(plant)}
                className="plant-option"
              >
                <h3>{plant.common_name} ({plant.scientific_name})</h3>
              </div>
            ))}
          </div>
  
          <div className="modal-actions">
            <button 
              onClick={onClose}
              className="cancel-button"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
}