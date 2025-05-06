import { PlantInGarden } from '../types/models';

type Props = {
    plant: Partial<PlantInGarden>;
};

export default function FullPlantInfo({ plant }: Props) {
  return (
    <div className="full-plant-info">
        <p><strong>Scientific Name:</strong> {plant.scientific_name}</p>
        <p><strong>Year:</strong> {plant.year || 'N/A'}</p>
        <p><strong>Family:</strong> {plant.family || 'N/A'}</p>
        <p><strong>Genus:</strong> {plant.genus || 'N/A'}</p>

        <p><strong>Soil moisture:</strong> {plant.soil_moisture || 'N/A'}</p>
        <p><strong>Soil Texture:</strong> {plant.soil_texture || 'N/A'}</p>
        <p><strong>Soil Nutrients:</strong> {plant.soil_nutriments || 'N/A'}</p>
        <p><strong>Soil Salinity:</strong> {plant.soil_salinity || 'N/A'}</p>
        <p><strong>pH Range:</strong> {plant.ph_min} - {plant.ph_max}</p>

        <p><strong>Sunlight:</strong> {plant.sunlight || 'N/A'}</p>
        <p><strong>Temperature Range:</strong> {plant.min_temp}° to {plant.max_temp}°</p>
        <p><strong>Days to Harvest:</strong> {plant.days_to_harvest || 'N/A'}</p>

        <p><strong>Edible:</strong> {plant.edible ? 'Yes' : 'No'}</p>
        <p><strong>Growth Rate:</strong> {plant.growth_rate || 'N/A'}</p>
        <p><strong>Max Height:</strong> {plant.max_height || 'N/A'} cm</p>
        <p><strong>Average Height:</strong> {plant.avg_height || 'N/A'} cm</p>
        <p><strong>Growth Months:</strong> {plant.growth_months?.join(', ') || 'N/A'}</p>
        <p><strong>Row Spacing:</strong> {plant.row_spacing?.join(', ')} cm</p>
    </div>
  );
}
