import requests
from django.core.management.base import BaseCommand
from bloom.models import Plant
import os
import time
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloom.settings')

PLANTS_TO_FETCH = [
    "Rose", "Tulip", "Lavender", "Bonsai Tree", 
    "Snake Plant", "Spider Plant", "Peace Lily", 
    "Fiddle Leaf Fig", "Aloe Vera", "Pothos", 
    "ZZ Plant", "Rubber Plant", "Monstera Deliciosa", 
    "English Ivy", "Chinese Evergreen", "Philodendron", 
    "Dracaena", "Cast Iron Plant", "Boston Fern", 
    "Calathea", "Orchid", "Jade Plant", "Sunflower"
]

def fetch_plant_by_name(common_name):
    url = f"https://trefle.io/api/v1/plants/search?token={TOKEN}&q={common_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Exception raised for 4XX/5XX responses (client or server errors)
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {common_name}: {e}")
        return []

def get_plant_details(self_link):
    url = f'https://trefle.io{self_link}?token={TOKEN}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('data', {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching plant details: {e}")
        return {}

def save_plant(plant_data, detailed_data=None):
    
    # Basic plant info
    plant_info = {
        'common_name': plant_data.get('common_name', 'Unknown'),
        'scientific_name': plant_data.get('scientific_name'),
        'year': plant_data.get('year'),
        'genus_id': plant_data.get('genus_id'),
        'family': plant_data.get('family'),
        'genus': plant_data.get('genus'),
    }

    # Detailed plant info
    field_mapping = {
            'growth_rate': 'growth_rate',
            'maximum_height': 'max_height',
            'average_height': 'avg_height',
            'growth_months': 'growth_months',
            'row_spacing': 'row_spacing',
            'spread': 'spread',
            'toxicity': 'toxicity',
            'soil_humidity': 'soil_humidity',
            'soil_texture': 'soil_texture',
            'soil_nutriments': 'soil_nutriments',
            'soil_salinity': 'soil_salinity',
            'ph_maximum': 'ph_max',
            'ph_minimum': 'ph_min',
            'light': 'sunlight',
            'maximum_temperature': 'max_temp',
            'minimum_temperature': 'min_temp',
            'days_to_harvest': 'days_to_harvest',
            'atmospheric_humidity': 'atmospheric_humidity',
            'minimum_precipitation': 'min_precipitation',
            'maximum_precipitation': 'max_precipitation',
            'minimum_root_depth': 'min_root_depth',
            'bloom_months': 'bloom_months',
            'fruit_months': 'fruit_months',
            'ligneous_type': 'ligneous_type'
    }
    for api_field, model_field in field_mapping.items():
            if api_field in detailed_data:
                plant_info[model_field] = detailed_data.get(api_field)

    
    # if detailed_data:
    #     # Derail attributes 
    #     detail_keys = [
    #         'duration', 'vegetable', 'growth_rate', 'avg_height', 'toxicity',
    #         'maximum_height', 'toxicity', 'light', 'color', 'growth_rate', 'maximum_height',
    #         'maximum_temperature', 'minimum_temperature', 'ph_maximum', 'ph_minimum',
    #         'bloom_months', 'fruit_months', 'edible', 'edible_parts', 'vegetable',
    #         'soil_humidity', 'soil_texture', 'soil_nutriments', 'soil_salinity', 
    #         'light', 'row_spacing', 'days_to_harvest', 'atmospheric_humidity', 
    #         'maximum_precipitation', 'minimum_precipitation', 'bloom_months', 'fruit_months', 
    #         'ligneous_type', 
    #     ]
        
    #     for key in detail_keys:
    #         if key in detailed_data:
    #             plant_info[key] = detailed_data.get(key)
    
    # Save/ Update
    try:
        Plant.objects.update_or_create(
            scientific_name=plant_info['scientific_name'],  
            defaults=plant_info
        )
        print(f"Saved: {plant_info['common_name']} ({plant_info['scientific_name']})")
        return True
    except Exception as e:
        print(f"Error saving plant {plant_info.get('scientific_name')}: {e}")
        return False

def fetch_and_save_plants():
    print(f"Starting to fetch data for {len(PLANTS_TO_FETCH)} plants...")
    
    plants_processed = 0
    plants_added = 0
    
    for common_name in PLANTS_TO_FETCH:
        print(f"\nSearching for: {common_name}")
        plants = fetch_plant_by_name(common_name)
        
        if not plants:
            print(f"No results found for '{common_name}'")
            continue
            
        # First result
        plant = plants[0]
        plants_processed += 1
        
        detailed_data = None
        self_link = plant.get('links', {}).get('self')
        if self_link:
            print(f"Fetching detailed information...")
            detailed_data = get_plant_details(self_link)
            
        time.sleep(1)
        
        if save_plant(plant, detailed_data):
            plants_added += 1
    
    print(f"\nCompleted! Processed {plants_processed} plants and added/updated {plants_added} plants in the database.")

class Command(BaseCommand):
    help = 'Fetch plant data from Trefle API and store in database'

    def handle(self, *args, **kwargs):
        fetch_and_save_plants()
        self.stdout.write(self.style.SUCCESS('Plant data fetch completed!'))


# For running script directly
if __name__ == "__main__":
    fetch_and_save_plants()