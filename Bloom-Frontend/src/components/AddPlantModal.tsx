type Props = {
    customName: string;
    sensor: number;
    isSensorTaken: (sensorId: number) => boolean;
    onCustomNameChange: (name: string) => void;
    onSensorChange: (sensorId: number) => void;
    onCancel: () => void;
    onSave: () => void;
    customNameError: boolean;
    autoWatering: boolean;
    onAutoWateringChange: (value: boolean) => void;
  };
  
  export default function AddPlantModal({
    customName,
    sensor,
    isSensorTaken,
    onCustomNameChange,
    onSensorChange,
    onCancel,
    onSave,
    customNameError,
    autoWatering,
    onAutoWateringChange,
  }: Props) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h2>Add Plant to Garden</h2>
  
          <div className="form-group">
            <label>Custom Name</label>
            <input
              type="text"
              value={customName}
              onChange={(e) => onCustomNameChange(e.target.value)}
              placeholder="Enter custom plant name"
              style={{ borderColor: customNameError ? 'red' : undefined }}
            />
            {customNameError && (
              <div className="error-message" style={{ color: 'red' }}>
                Add custom name
              </div>
            )}
          </div>
  
          <div className="form-group">
            <label>Sensor ID</label>
            <input
              type="number"
              value={sensor}
              onChange={(e) => onSensorChange(Number(e.target.value))}
              placeholder="Enter sensor ID"
              min="0"
            />
            {isSensorTaken(sensor) && (
              <div className="error-message" style={{ color: 'red' }}>
                This sensor ID is already taken.
              </div>
            )}
          </div>

          <div className="form-group" style={{ marginTop: '10px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <input
                type="checkbox"
                checked={autoWatering}
                onChange={(e) => onAutoWateringChange(e.target.checked)}
                style={{ width: '16px', height: '16px' }}
              />
              Auto-Watering 
            </label>
          </div>

          <div className="modal-actions">
            <button onClick={onCancel} className="cancel-button">Cancel</button>
            <button onClick={onSave} className="confirm-button" disabled={isSensorTaken(sensor)}>
              Save Plant
            </button>
          </div>
        </div>
      </div>
    );
  }