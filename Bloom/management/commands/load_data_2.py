import requests
from django.core.management.base import BaseCommand
from bloom.models import Plant
import os
import time
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TREFLE_API_TOKEN')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloom.settings')

popular_plants = ["Rose", "Tulip", "Lavender", "Bonsai Tree", 
    "Snake Plant (Sansevieria)", 
    "Spider Plant (Chlorophytum comosum)", 
    "Peace Lily (Spathiphyllum)", 
    "Fiddle Leaf Fig (Ficus lyrata)", 
    "Aloe Vera", 
    "Pothos (Epipremnum aureum)", 
    "ZZ Plant (Zamioculcas zamiifolia)", 
    "Rubber Plant (Ficus elastica)", 
    "Monstera Deliciosa", 
    "English Ivy (Hedera helix)", 
    "Chinese Evergreen (Aglaonema)", 
    "Philodendron", 
    "Dracaena", 
    "Cast Iron Plant (Aspidistra elatior)", 
    "Boston Fern (Nephrolepis exaltata)", 
    "Calathea", 
    "Orchid", 
    "Succulents (e.g., Echeveria, Jade Plant)", 
    "African Violet (Saintpaulia)"]

def fetch_plant_by_name(common_name):
    url = f"https://trefle.io/api/v1/plants/search"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    params = {
        "q": common_name
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Error fetching {common_name}: {response.status_code}")
        return []

def plant_exists(scientific_name):
    return Plant.objects.filter(scientific_name=scientific_name).exists()

def extract_plant_basic(plants):
    for plant in plants:
        common_name = plant.get('common_name')
        if not common_name:
            common_name = "Unknown"

        Plant.objects.update_or_create(
            common_name=common_name,
            scientific_name=plant.get('scientific_name'),  # Minimum identifier is scientific name
            year=plant.get('year'),
            genus_id=plant.get('genus_id'),
            family=plant.get('family'),
            genus=plant.get('genus'),
        )

# Extract detailed plant data using self link
def get_plant_self_link(self_link):
    url = f'https://trefle.io{self_link}'
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', {})
    else:
        print(f"Error fetching detailed data: {response.status_code}")
        return {}

# Extracts detailed plant information
def extract_plant_detailed(plant):
    keys = [
        'shape_and_orientation', 'edible', 'edible_part', 'duration', 'observation', 'vegetable', 
        'leaf_retention', 'texture', 'conspicuous', 'shape', 'color', 'growth_rate', 'maximum_height', 
        'avg_height', 'toxicity', 'soil_humidity', 'soil_texture', 'soil_nutriments', 'soil_salinity', 
        'ph_maximum', 'ph_minimum', 'light', 'maximum_temperature', 'minimum_temperature', 
        'minimum_root_depth', 'spread', 'row_spacing', 'days_to_harvest', 'atmospheric_humidity', 
        'maximum_precipitation', 'minimum_precipitation', 'bloom_months', 'fruit_months', 
        'ligneous_type'
    ]

    self_link = plant.get('links', {}).get('self') 
    if self_link:
        detailed_data = get_plant_self_link(self_link)

        # Update detailed information
        data = {key: detailed_data.get(key) for key in keys}
        Plant.objects.update_or_create(
            scientific_name=plant.get('scientific_name'),
            defaults=data
        )

def last_page():
    if os.path.exists('page.txt'):
        with open('page.txt', 'r') as f:
            return int(f.read())
    return 1  

def fetch_plant_data():
    for common_name in popular_plants:
        print(f"Fetching data for {common_name}...")
        
        plants = fetch_plant_by_name(common_name)

        for plant in plants:
            scientific_name = plant.get('scientific_name')
            
            if scientific_name and not plant_exists(scientific_name):
                extract_plant_basic([plant]) 
                extract_plant_detailed(plant)
            
class Command(BaseCommand):
    help = 'Fetch plant data from Trefle API and store in database'

    def handle(self, *args, **kwargs):
        print("Starting to fetch plant data...")
        fetch_plant_data()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored plant data!'))
