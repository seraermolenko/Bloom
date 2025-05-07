import { PlantInGarden } from '../types/models';

type Props = {
  plant: Partial<PlantInGarden>;
};

const getPercentage = (val: number | null | undefined) => {
  return val !== null && val !== undefined ? `${val * 10}%` : 'N/A';
};

const moistureLabel = (val: number | null | undefined) => {
  if (val === null || val === undefined) return 'N/A';
  if (val <= 2) return 'Dry';
  if (val <= 5) return 'Moderate';
  if (val <= 8) return 'Moist';
  return 'Saturated';
};

const textureLabel = (val: number | null | undefined) => {
  if (val === null || val === undefined) return 'N/A';
  if (val <= 3) return 'Xerophile';
  if (val <= 6) return 'Loamy';
  return 'Subaquatic';
};

const nutrientsLabel = (val: number | null | undefined) => {
  if (val === null || val === undefined) return 'N/A';
  if (val <= 3) return 'Oligotrophic';
  if (val <= 6) return 'Mesotrophic';
  return 'Hypereutrophic';
};

const salinityLabel = (val: number | null | undefined) => {
  if (val === null || val === undefined) return 'N/A';
  if (val <= 3) return 'Untolerant';
  if (val <= 6) return 'Moderately Tolerant';
  return 'Hyperhaline';
};

const sunlightLabel = (val: number | null | undefined) => {
  if (val === null || val === undefined) return 'N/A';
  if (val <= 2) return 'Low Light';
  if (val <= 6) return 'Partial Sun';
  return 'Full Sun';
};

const humidityLabel = (val: number | null | undefined) => {
  if (val === null || val === undefined) return 'N/A';
  if (val <= 3) return 'Dry';
  if (val <= 6) return 'Moderate';
  return 'Very Humid';
};

export default function FullPlantInfo({ plant }: Props) {
  return (
    <div className="full-plant-info">
      <div style={{ margin: '32px 0' }}>
        <h3 style={{ color: 'var(--pine-dark)', marginBottom: '12px' }}>🌿 Basic Info</h3>
        <p><strong>Scientific Name:</strong> {plant.scientific_name}</p>
        <p><strong>Year:</strong> {plant.year || 'N/A'}</p>
        <p><strong>Family:</strong> {plant.family || 'N/A'}</p>
        <p><strong>Genus:</strong> {plant.genus || 'N/A'}</p>
      </div>

      <div style={{ margin: '32px 0' }}>
        <h3 style={{ color: 'var(--pine-dark)', marginBottom: '12px' }}>🪴 Soil Info</h3>
        <p><strong>Soil Moisture:</strong>{' '}
          <span title="0 = dry (clay), 10 = saturated (rock)">
            {getPercentage(plant.soil_moisture)} ({moistureLabel(plant.soil_moisture)})
          </span>
        </p>
        <p><strong>Soil Texture:</strong>{' '}
          <span title="0 = xerophile, 10 = subaquatic">
            {getPercentage(plant.soil_texture)} ({textureLabel(plant.soil_texture)})
          </span>
        </p>
        <p><strong>Soil Nutrients:</strong>{' '}
          <span title="0 = oligotrophic, 10 = hypereutrophic">
            {getPercentage(plant.soil_nutriments)} ({nutrientsLabel(plant.soil_nutriments)})
          </span>
        </p>
        <p><strong>Soil Salinity:</strong>{' '}
          <span title="0 = untolerant, 10 = hyperhaline">
            {getPercentage(plant.soil_salinity)} ({salinityLabel(plant.soil_salinity)})
          </span>
        </p>
        <p><strong>pH Range:</strong> {plant.ph_min} - {plant.ph_max}</p>
      </div>

      <div style={{ margin: '32px 0' }}>
        <h3 style={{ color: 'var(--pine-dark)', marginBottom: '12px' }}>☀️ Environmental Needs</h3>
        <p><strong>Sunlight:</strong>{' '}
          <span title="0 = low light, 10 = very intense light">
            {getPercentage(plant.sunlight)} ({sunlightLabel(plant.sunlight)})
          </span>
        </p>
        <p><strong>Temperature Range:</strong> {plant.min_temp}° to {plant.max_temp}°</p>
        <p><strong>Atmospheric Humidity:</strong>{' '}
          <span title="0 = ≤10% humidity, 10 = ≥90% humidity">
            {getPercentage(plant.atmospheric_humidity)} ({humidityLabel(plant.atmospheric_humidity)})
          </span>
        </p>
      </div>

      <div style={{ margin: '32px 0' }}>
        <h3 style={{ color: 'var(--pine-dark)', marginBottom: '12px' }}>🌱 Growth Details</h3>
        <p><strong>Days to Harvest:</strong> {plant.days_to_harvest || 'N/A'}</p>
        <p><strong>Growth Rate:</strong> {plant.growth_rate || 'N/A'}</p>
        <p><strong>Growth Months:</strong> {plant.growth_months?.join(', ') || 'N/A'}</p>
        <p><strong>Bloom Months:</strong> {plant.bloom_months?.join(', ') || 'N/A'}</p>
        <p><strong>Fruit Months:</strong> {plant.fruit_months?.join(', ') || 'N/A'}</p>
        <p><strong>Max Height:</strong> {plant.max_height || 'N/A'} cm</p>
        <p><strong>Average Height:</strong> {plant.avg_height || 'N/A'} cm</p>
        <p><strong>Row Spacing:</strong> {plant.row_spacing?.join(', ')} cm</p>
        <p><strong>Min Root Depth:</strong> {plant.min_root_depth?.join(', ') || 'N/A'} cm</p>
      </div>

      <div style={{ margin: '32px 0' }}>
        <h3 style={{ color: 'var(--pine-dark)', marginBottom: '12px' }}>🍓 Edibility & Traits</h3>
        <p><strong>Edible:</strong> {plant.edible === true ? 'Yes' : plant.edible === false ? 'No' : 'N/A'}</p>
        <p><strong>Toxicity:</strong> {plant.toxicity || 'N/A'}</p>
      </div>
    </div>
  );
}