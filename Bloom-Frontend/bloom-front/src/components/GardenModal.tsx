type Props = {
    gardenName: string;
    setGardenName: (val: string) => void;
    onClose: () => void;
    onConfirm: () => void;
  };
  
export default function GardenModal({ gardenName, setGardenName, onClose, onConfirm }: Props) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h2>Create New Garden</h2>
          <div className="form-group">
            <label>Garden Name</label>
            <input
              type="text"
              value={gardenName}
              onChange={(e) => setGardenName(e.target.value)}
              placeholder="e.g. 'Living Room Herbs'"
            />
          </div>
          <div className="modal-actions">
            <button onClick={onClose} className="cancel-button">Cancel</button>
            <button onClick={onConfirm} className="confirm-button" disabled={!gardenName.trim()}>
              Create Garden
            </button>
          </div>
        </div>
      </div>
    );
}
  