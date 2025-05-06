import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Garden, PlantInGarden } from '../types/models';
import SearchModal from '../components/SearchModal';
import PersonalPlantDetailsModal from '../components/PersonalPlantDetailsModal';
import ConfirmDeleteModal from '../components/ConfirmDeleteModal';
import SettingsModal from '../components/SettingsModal';
import AddPlantModal from '../components/AddPlantModal';
import { usePlantSearch } from '../hooks/usePlantSearch';
import { useSavePlant } from '../hooks/useSavePlant';
import '../App.css';

export default function GardenPage() {
    const { id } = useParams();
    const [garden, setGarden] = useState<Garden | null>(null);
    const [loading, setLoading] = useState(true);
    const [showAddPlantModal, setShowAddPlantModal] = useState(false);
    const [showSearchModal, setShowSearchModal] = useState(false);
    const [showSettingsModal, setShowSettingsModal] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const [showPlantDeleteConfirm, setShowPlantDeleteConfirm] = useState(false);
    const [selectedPlant, setSelectedPlant] = useState<number | null>(null);
    const [selectedPersonalPlant, setSelectedPersonalPlant] = useState<PlantInGarden | null>(null);
    const [customName, setCustomName] = useState('');
    const [takenSensors, setTakenSensors] = useState<number[]>([]);
    const [sensor, setSensor] = useState<number>(0);
    const navigate = useNavigate();
    const [customNameError, setCustomNameError] = useState(false);
  
    useEffect(() => {
      if (!id) return; 
      const fetchGarden = async () => {
        try {
          const response = await fetch(`/get_garden/?garden_id=${id}`);
          if (!response.ok) throw new Error('Garden not found');
          const data = await response.json();
          console.log("Fetched garden data:", data);
          const updatedPlants = data.plants.map((plant: PlantInGarden) => ({
            ...plant,
            date_added: new Date(plant.date_added), 
          }));
          setGarden({ ...data, plants: updatedPlants });
        } catch (error) {
          console.error('Error fetching garden:', error);
        } finally {
          setLoading(false);
        }
      };
  
      fetchGarden();
    }, [id]);
  
    useEffect(() => {
      const fetchTakenSensors = async () => {
        try {
          const response = await fetch(`/taken_sensors/`);
          const data = await response.json();
          setTakenSensors(data); 
        } catch (error) {
          console.error('Error fetching available sensors:', error);
        }
      };
  
      fetchTakenSensors();
    }, []);


    const fetchGardenData = async () => {
      if (!id) return;
      console.log('Garden ID:', id); 
      setLoading(true);
      try {
        const response = await fetch(`/get_garden/?garden_id=${id}`);
        if (!response.ok) throw new Error('Garden not found');
        const data = await response.json();
        console.log('Fetched garden data:', data);
        const updatedPlants = data.plants.map((plant: PlantInGarden) => ({
          ...plant,
          date_added: new Date(plant.date_added), 
        }));
        setGarden({ ...data, plants: updatedPlants });
      } catch (error) {
        console.error('Error fetching garden:', error);
      } finally {
        setLoading(false);
      }
    };


    useEffect(() => {
      fetchGardenData(); 
      const ws = new WebSocket(`ws://localhost:8000/ws/garden/${id}/`);

      ws.onopen = () => {
        console.log(" WebSocket opened");
      };
    
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (
          data &&
          data.updated_plant &&
          typeof data.updated_plant.sensor_id === "number" &&
          typeof data.updated_plant.status === "string" &&
          typeof data.updated_plant.garden_id === "number"
        ){
          console.log('Received update via WebSocket:', data);
    
        
          if (data.updated_plant.garden_id === Number(id)) {
            setGarden((prevGarden) => {
              if (!prevGarden) return null;
    
              const updatedPlants = prevGarden.plants.map((plant) => {
                if (plant.sensor_id === data.updated_plant.sensor_id) {
                  console.log(" Updating plant status in UI:", plant.sensor_id, "=>", data.updated_plant.status);
                  return { ...plant, status: data.updated_plant.status }; 
                }
                return plant;
              });
    
              return { ...prevGarden, plants: updatedPlants }; 
            });
          }
        } else {
          console.warn("Invalid WebSocket payload shape:", data);
        }
      };
    
      ws.onerror = (err) => {
        if (ws.readyState !== WebSocket.OPEN) {
          console.warn("WebSocket error (connection may have closed too early):", err);
        }
        else{console.error('WebSocket error:', err);}
      };
    
      return () => ws.close();
    }, [id]);    

  
    const {
      searchTerm,
      setSearchTerm,
      availablePlants,
      setAvailablePlants, 
      handleSearch
    } = usePlantSearch();

    const { handleSavePlant } = useSavePlant();

    const resetInputs = () => {
      setSelectedPlant(null);
      setCustomName('');
      setSensor(0);
    };
  
    const openSearchModal = () => {
      setSelectedPlant(null);  
      setCustomName('');
      setSensor(0);  
      setSearchTerm('');  
      setShowSearchModal(true); 
      setAvailablePlants([]); 
    };
  
    const isSensorTaken = (sensorId: number) => {
      if (sensorId === 0) return false; 
      return takenSensors.includes(sensorId);
    };
  
    const handleDeleteGarden = async () => {
      if (!id) return;
  
      try {
        const response = await fetch(`/delete_garden/?garden_id=${id}`, {
          method: 'DELETE',
        });
  
        if (!response.ok) throw new Error('Failed to delete garden');
  
        navigate('/');
      } catch (error) {
        console.error('Error deleting garden:', error);
        alert('Failed to delete garden');
      }
    };
  
    const handleDeletePersonalPlant = async () => {
      if (!selectedPersonalPlant) return;
  
      try {
        const response = await fetch('/personal_plants/delete/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            personal_plant_id: selectedPersonalPlant.personal_plant_id
          }),
        });
  
        if (!response.ok) throw new Error('Failed to delete plant');
  
        const gardenResponse = await fetch(`/get_garden/?garden_id=${id}`);
        if (!gardenResponse.ok) throw new Error('Failed to fetch updated garden');
        await gardenResponse.json();
        
        const sensorId = selectedPersonalPlant.sensor_id;
        if (sensorId) {
          setTakenSensors((prevSensors) => prevSensors.filter((sensor) => sensor !== sensorId));
        }
        fetchGardenData();
        
        setSelectedPersonalPlant(null);
        setShowPlantDeleteConfirm(false);
      } catch (error) {
        console.error('Error deleting plant:', error);
        alert('Failed to delete plant');
      }
    };
  
  
    if (loading) return <div>Loading...</div>;
    if (!garden) return <div>Garden not found</div>;
  
    return (
      <div className="garden-page">
        <div className="garden-header">
          <h1>{garden.name}</h1>
          <button 
            className="settings-button"
            onClick={() => setShowSettingsModal(true)}
          >
            More
          </button>
        </div>
        <Link to="/" className="back-to-home">Back to Home</Link>
        
        <div className="plants-container">
          {garden.plants
          .sort((a, b) => {
            const dateA = new Date(a.date_added).getTime();
            const dateB = new Date(b.date_added).getTime();
            return dateA - dateB;
          })
          .map(plant => (
            <div 
              key={plant.personal_plant_id} 
              className="plant-card"
              onClick={() => setSelectedPersonalPlant(plant)}
            >
              <h3>{plant.custom_name || plant.common_name}</h3>
              <p>{plant.common_name}</p>
              <p>Auto Watering: {plant.auto_watering ? 'On' : 'Off'}</p>
              {plant.sensor_id !== 0 && (<p ><strong className={plant.status === 'Thirsty' ? 'breathing' : ''}>{plant.status || 'No status'}</strong></p>)}
              {plant.sensor_id === 0 && (<p><strong>{' - '}</strong></p>)}
            </div>
          ))}
          <div 
            className="add-plant-box"
            onClick={openSearchModal}
          >
            <span>+ Add Plant</span>
          </div>
        </div>
  
        {selectedPersonalPlant && (
            <PersonalPlantDetailsModal 
              personalPlant={selectedPersonalPlant}
              onClose={() => setSelectedPersonalPlant(null)}
              onDelete={() => setShowPlantDeleteConfirm(true)}
            />
        )}
  
        {showPlantDeleteConfirm && (
          <ConfirmDeleteModal 
            title="Confirm Delete"
            message="Are you sure you want to delete this plant? This action cannot be undone."
            onCancel={() => setShowPlantDeleteConfirm(false)}
            onConfirm={handleDeletePersonalPlant}
          />
        )}
  
        {showSearchModal && (
            <SearchModal
                searchTerm={searchTerm}
                availablePlants={availablePlants}
                onChangeSearch={handleSearch}
                onClose={() => setShowSearchModal(false)}
                onSelectPlant={(plantId) => {
                    setSelectedPlant(plantId);
                    setShowSearchModal(false);
                    setShowAddPlantModal(true);
                    setAvailablePlants([]);  
                  }}
            />
        )}
              
        {showAddPlantModal && (
          <AddPlantModal
            customName={customName}
            sensor={sensor}
            onCustomNameChange={setCustomName}
            onSensorChange={setSensor}
            onCancel={() => setShowAddPlantModal(false)}
            onSave={() => {
              if (!customName.trim()) {
                setCustomNameError(true);
                return;
              }
              handleSavePlant({
                selectedPlant,
                customName,
                sensor,
                gardenId: id,
                setGarden,
                setShowAddPlantModal,
                resetInputs,
              })
              fetchGardenData(); 
            }}
            isSensorTaken={isSensorTaken}
            customNameError={customNameError}
          />
        )}

        {showSettingsModal && (
          <SettingsModal
            onClose={() => setShowSettingsModal(false)}
            onDelete={() => {
              setShowSettingsModal(false);
              setShowDeleteConfirm(true);
            }}
          />
        )}
  
        {showDeleteConfirm && (
          <ConfirmDeleteModal
            title="Confirm Delete"
            message="Are you sure you want to delete this garden?"
            onCancel={() => {
              setShowDeleteConfirm(false);
              setShowSettingsModal(true);
            }}
            onConfirm={handleDeleteGarden}
          />
        )}
      </div>
    );
  };