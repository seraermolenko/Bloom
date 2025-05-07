import { useState } from 'react';

interface SavePlantParams {
  selectedPlant: number | null;
  customName: string;
  sensor: number;
  gardenId: string | undefined;
  setGarden: (garden: any) => void;
  setShowAddPlantModal: (show: boolean) => void;
  resetInputs: () => void;
  autoWatering: boolean;
}

export function useSavePlant() {
  const [saving, setSaving] = useState(false);

  const handleSavePlant = async ({
    selectedPlant,
    customName,
    sensor,
    gardenId,
    setGarden,
    setShowAddPlantModal,
    resetInputs,
    autoWatering,
  }: SavePlantParams) => {
    if (!selectedPlant || !customName) {
      alert('Please fill in all required fields.');
      return;
    }

    setSaving(true);

    try {
      const response = await fetch('/personal_plants/create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plant_id: selectedPlant,
          garden_id: gardenId,
          custom_name: customName,
          sensor_id: sensor,
          auto_watering: autoWatering,
        }),
      });

      if (!response.ok) throw new Error('Failed to add plant');

      const updatedGardenResponse = await fetch(`/get_garden/?garden_id=${gardenId}`);
      if (!updatedGardenResponse.ok) throw new Error('Failed to fetch updated garden');
      const updatedGarden = await updatedGardenResponse.json();

      setGarden(updatedGarden);
      setShowAddPlantModal(false);
      resetInputs();
    } catch (error) {
      console.error('Error saving plant:', error);
      alert('Failed to add plant');
    } finally {
      setSaving(false);
    }
  };

  return { handleSavePlant, saving };
}
