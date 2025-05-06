type Props = {
  onClose: () => void;
  onDelete: () => void;
};

export default function SettingsModal({ onClose, onDelete }: Props) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Settings</h2>
        <div className="settings-options">
          <button className="delete-garden-button" onClick={onDelete}>Delete Garden</button>
        </div>
        <div className="modal-actions">
          <button onClick={onClose} className="cancel-button">Close</button>
        </div>
      </div>
    </div>
  );
}