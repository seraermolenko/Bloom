import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Garden, PlantInGarden} from '../types/models';
import { usePlantSearch } from '../hooks/usePlantSearch';
import GardenModal from '../components/GardenModal';
import ExploreModal from '../components/ExploreModal';
import PlantDetailsModal from '../components/PlantDetailsModal';
import '../App.css';

export default function HomePage() {
  const [gardens, setGardens] = useState<Garden[]>([]);
  const [showGardenModal, setShowGardenModal] = useState(false);
  const [gardenName, setGardenName] = useState('');
  const [showExploreModal, setShowExploreModal] = useState(false);
  const [selectedPlant, setSelectedPlant] = useState<Partial<PlantInGarden> | null>(null);
  const [showPlantDetails, setShowPlantDetails] = useState(false);

  useEffect(() => {
    const fetchUserGardens = async () => {
      try {
        console.log('Calling /get_user_gardens...');
        const response = await fetch('/get_user_gardens/?user_id=1'); 
        if (!response.ok) throw new Error('Failed to fetch gardens');
        const data = await response.json();
        setGardens(data);
      } catch (error) {
        console.error('Error loading gardens:', error);
      }
    };

    fetchUserGardens();
  }, []);

  const handleAddGarden = async () => {
    if (!gardenName.trim()) return;

    try {
      const response = await fetch('/create_garden/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: gardenName,
          private: false,
          user_id: 1
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create garden');
      }

      const newGarden = await response.json();

      setGardens((prev) => [...prev, newGarden]);
      setGardenName('');
      setShowGardenModal(false);

    } catch (error) {
      console.error('Error creating garden:', error);
      alert('Failed to create garden');
    }
  };

  const {
    searchTerm,
    setSearchTerm,
    availablePlants,
    handleSearch,
    setAvailablePlants, 
  } = usePlantSearch();

  const handlePlantSelect = async (plant: any) => {
    try {
      const response = await fetch(`/get_plant_by_id/?plant_id=${plant.id}`);
      if (!response.ok) throw new Error("Failed to fetch full plant data");
  
      const fullPlant = await response.json();
      setSelectedPlant(fullPlant);
      setShowPlantDetails(true);
    } catch (error) {
      console.error("Error loading full plant info:", error);
      alert("Unable to load full plant details.");
    }
  };

  const openExploreModal = () => {
    setSearchTerm(''); 
    setShowExploreModal(true);
    setAvailablePlants([]); 
  };

  return (
    <>
      <h1 className="header">Bloom</h1>

      <div className="gardens-container">
        {gardens.map((garden) => (
          <Link to={`/garden/${garden.garden_id}`} key={garden.garden_id} className="garden-box">
            <h3>{garden.name}</h3>
          </Link>
        ))}
        
        {gardens.length < 6 && (
          <div 
            className="add-garden-box"
            onClick={() => setShowGardenModal(true)}
          >
            <span>+ Add Garden</span>
          </div>
        )}
      </div>

      <button 
        className="explore-plants-button"
        onClick={openExploreModal}  // Open the modal and reset search state
      >
        Explore Plants
      </button>

      {showGardenModal && (
        <GardenModal
          gardenName={gardenName}
          setGardenName={setGardenName}
          onClose={() => setShowGardenModal(false)}
          onConfirm={handleAddGarden}
        />
      )}

      {showExploreModal && (
        <ExploreModal
          searchTerm={searchTerm}
          availablePlants={availablePlants}
          onClose={() => {
            setShowExploreModal(false);
            setSearchTerm('');
            setAvailablePlants([]);  
          }}
          onChangeSearch={handleSearch}
          onSelectPlant={handlePlantSelect}
        />
      )}

      {showPlantDetails && selectedPlant && (
        <PlantDetailsModal 
          plant={selectedPlant}
          onClose={() => {
            setShowPlantDetails(false);
            setShowExploreModal(false);
            setSelectedPlant(null);
            setSearchTerm('');
          }}
          onBackToSearch={() => {
            setShowPlantDetails(false);
            setSelectedPlant(null);
            setShowExploreModal(true);
          }}
        />
      )}
    </>
);
} 


  

