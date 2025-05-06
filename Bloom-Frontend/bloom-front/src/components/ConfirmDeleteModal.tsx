type Props = {
    title: string;
    message: string;
    onCancel: () => void;
    onConfirm: () => void;
  };
  
  export default function ConfirmDeleteModal({ title, message, onCancel, onConfirm }: Props) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h2>{title}</h2>
          <p>{message}</p>
          <div className="modal-actions">
            <button onClick={onCancel} className="cancel-button">Cancel</button>
            <button onClick={onConfirm} className="delete-button">Delete</button>
          </div>
        </div>
      </div>
    );
  }
  