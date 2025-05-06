type Props = {
  searchTerm: string;
  availablePlants: any[];
  onClose: () => void;
  onChangeSearch: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSelectPlant: (plantId: number) => void;
};

export default function SearchModal({
  searchTerm,
  availablePlants,
  onClose,
  onChangeSearch,
  onSelectPlant,
}: Props)
{
  return (
      <div className="modal-overlay">
          <div className="modal">
            <h2>Select Plant</h2>

            <div className="form-group">
              <label>Search Plants by Name</label>
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
                  onClick={() => onSelectPlant(plant.id)}
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
                Cancel
              </button>
            </div>
          </div>
        </div>
  )
}