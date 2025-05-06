export type PlantInGarden = {
    personal_plant_id: number;
    custom_name: string | null;
    sensor_id: number | null;
    status: string | null;
    auto_watering: boolean;
    last_watered: Date | null;
    date_added: Date;

    garden_id: number;
    plant_id: number;
    common_name: string;
  
    scientific_name: string;
    year: number | null;
    family: string | null;
    genus: string | null;
    genus_id: number | null;
    edible: boolean | null;
    edible_parts: string[] | null;
    vegetable: boolean | null;
    growth_rate: string | null;
    max_height: number | null;
    avg_height: number | null;
    growth_months: string[] | null;
    row_spacing: number[] | null;
    spread: number[] | null;
    toxicity: string | null;
    soil_moisture: number | null;
    soil_texture: number | null;
    soil_nutriments: number | null;
    soil_salinity: number | null;
    ph_max: number | null;
    ph_min: number | null;
    sunlight: number | null;
    max_temp: number | null;
    min_temp: number | null;
    days_to_harvest: number | null;
    atmospheric_moisture: number | null;
    min_precipitation: number[] | null;
    max_precipitation: number[] | null;
    min_root_depth: number[] | null;
    bloom_months: string[] | null;
    fruit_months: string[] | null;
    ligneous_type: string | null;
};
  
export type Garden = {
    garden_id: number;
    name: string;
    private: boolean;
    plants: PlantInGarden[];
};