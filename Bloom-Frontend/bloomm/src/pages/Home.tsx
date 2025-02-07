import '../App.css';
import { useState } from 'react';
import CreateGardenDialog from '../components/CreateGardenDialog';
import { Button } from '../components/ui/button';
import { PlusCircle } from 'lucide-react'; 
import PlantCard from '../components/PlantCard';
import GardenCard from '../components/GardenCard';

interface Garden {
  id: string;
  name: string;
  plants: Plant[];
}

interface Plant {
  id: string;
  name: string;
  species: string;
  image: string;
}

const Home = () => {
  const [gardens, setGardens] = useState<Garden[]>([]);
  const [selectedGarden, setSelectedGarden] = useState<Garden | null>(null);

  const handleCreateGarden = (name: string) => {
    const newGarden: Garden = {
      id: Date.now().toString(),
      name,
      plants: [],
    };
    setGardens([...gardens, newGarden]);
  };

  const handleAddPlant = (gardenId: string) => {
    // This is a placeholder plant - in a real app, you'd have a plant selection dialog
    const newPlant: Plant = {
      id: Date.now().toString(),
      name: "Beautiful Rose",
      species: "Rosa",
      image: "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07",
    };
    
    setGardens(gardens.map(garden => {
      if (garden.id === gardenId) {
        return { ...garden, plants: [...garden.plants, newPlant] };
      }
      return garden;
    }));
  };

  return (
    <div className="min-h-screen bg-garden-cream/50">
      <div className="container py-8 space-y-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-garden-soil">My Gardens</h1>
            <p className="text-garden-soil/80 mt-2">Create and manage your virtual gardens</p>
          </div>
          <CreateGardenDialog onCreateGarden={handleCreateGarden} />
        </div>

        {selectedGarden ? (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <button 
                  onClick={() => setSelectedGarden(null)}
                  className="text-garden-leaf hover:text-garden-leaf/80 transition-colors"
                >
                  ← Back to Gardens
                </button>
                <h2 className="text-2xl font-semibold text-garden-soil mt-2">{selectedGarden.name}</h2>
              </div>
              <Button 
                onClick={() => handleAddPlant(selectedGarden.id)}
                className="bg-garden-leaf text-white hover:bg-garden-leaf/90"
              >
                <PlusCircle className="mr-2 h-4 w-4" />
                Add Plant
              </Button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {selectedGarden.plants.map((plant) => (
                <PlantCard
                  key={plant.id}
                  {...plant}
                  onClick={() => {/* Show plant details */}}
                />
              ))}
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {gardens.map((garden) => (
              <GardenCard
                key={garden.id}
                name={garden.name}
                plantCount={garden.plants.length}
                onClick={() => setSelectedGarden(garden)}
              />
            ))}
            {gardens.length === 0 && (
              <div className="col-span-full text-center py-12 text-garden-soil/60">
                No gardens yet. Create your first garden to get started!
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;