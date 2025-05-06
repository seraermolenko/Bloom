import { useState } from 'react';

export function usePlantSearch() {
  const [searchTerm, setSearchTerm] = useState('');
  const [availablePlants, setAvailablePlants] = useState<any[]>([]);

  const handleSearch = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);

    if (value === '') {
      setAvailablePlants([]);
      return;
    }

    try {
      const response = await fetch(`/plants/search/?name=${value}`);
      if (!response.ok) {
        if (response.status === 404) {
          setAvailablePlants([]);
        } else {
          throw new Error('Failed to fetch plants');
        }
        return;
      }

      const data = await response.json();
      console.log('Search Result:', data);

      if (data.length === 0) {
        setAvailablePlants([]);
        alert('No plants found for your search!');
      } else {
        setAvailablePlants(data.slice(0, 4));
      }
    } catch (error) {
      console.error('Error searching plants:', error);
    }
  };

  return {
    searchTerm,
    setSearchTerm,
    availablePlants,
    setAvailablePlants, 
    handleSearch,
  };
}
