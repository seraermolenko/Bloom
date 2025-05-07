import requests
from django.core.management.base import BaseCommand
from bloom.models import Plant
import os
import time
from dotenv import load_dotenv
load_dotenv()
import json

TOKEN = os.getenv('TOKEN')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloom.settings')

PLANTS_TO_FETCH = [
    # Succulents
    "Echeveria elegans",         # Mexican snowball
    "Sedum morganianum",         # Burro's tail
    "Crassula ovata",            # Jade plant
    "Haworthia attenuata",       # Zebra plant
    "Aloe vera",                 # Aloe
    "Kalanchoe blossfeldiana",   # Flaming Katy
    "Senecio rowleyanus",        # String of pearls

    # Bonsai-friendly species
    "Ficus retusa",              # Common bonsai species
    "Juniperus procumbens",      # Japanese garden juniper
    "Ulmus parvifolia",          # Chinese elm
    "Pinus thunbergii",          # Japanese black pine
    "Acer palmatum",             # Japanese maple

    # Climbing/Trailing Houseplants
    "Epipremnum aureum",         # Golden pothos
    "Scindapsus pictus",         # Satin pothos
    "Philodendron hederaceum",   # Heartleaf philodendron
    "Monstera deliciosa",        # Swiss cheese plant
    "Syngonium podophyllum",     # Arrowhead vine
    "Hedera helix",              # English ivy

    # Common Indoor Foliage Plants
    "Zamioculcas zamiifolia",    # ZZ plant
    "Spathiphyllum wallisii",    # Peace lily
    "Ficus elastica",            # Rubber tree
    "Ficus lyrata",              # Fiddle-leaf fig
    "Aglaonema commutatum",      # Chinese evergreen
    "Calathea orbifolia",        # Calathea orbifolia
    "Dracaena marginata",        # Dragon tree
    "Chlorophytum comosum",      # Spider plant
    "Aspidistra elatior",        # Cast iron plant
    "Nephrolepis exaltata",      # Boston fern

    # Orchids
    "Phalaenopsis amabilis",     # Moth orchid
    "Dendrobium nobile",         # Noble dendrobium

    # Flowering Indoor Plants
    "Saintpaulia ionantha",      # African violet
    "Anthurium andraeanum",      # Flamingo flower
    "Begonia rex",               # Rex begonia

    # Common Vegetables
    "Solanum lycopersicum",      # Tomato
    "Capsicum annuum",           # Bell pepper
    "Cucumis sativus",           # Cucumber
    "Lactuca sativa",            # Lettuce
    "Daucus carota",             # Carrot
    "Spinacia oleracea",         # Spinach
    "Allium cepa",               # Onion
    "Allium sativum",            # Garlic
    "Pisum sativum",             # Garden pea
    "Phaseolus vulgaris",        # Green bean
    "Zea mays",                  # Corn
    "Beta vulgaris",             # Beetroot
    "Cucurbita pepo",            # Zucchini / Pumpkin
    "Brassica oleracea",         # Broccoli / Cabbage
    "Raphanus sativus",          # Radish
    "Brassica rapa",             # Turnip
    "Solanum melongena",         # Eggplant
    "Cichorium endivia",         # Endive
    "Cynara scolymus",           # Artichoke
    "Apium graveolens",          # Celery
    "Petroselinum crispum",      # Parsley

    # Culinary Herbs
    "Ocimum basilicum",          # Basil
    "Mentha spicata",            # Spearmint
    "Thymus vulgaris",           # Thyme
    "Rosmarinus officinalis",    # Rosemary
    "Origanum vulgare",          # Oregano
    "Coriandrum sativum",        # Cilantro
    "Salvia officinalis",        # Sage
    "Allium schoenoprasum",      # Chives
    "Lavandula angustifolia",    # Lavender
]



def fetch_plant_by_name(scientific_name):
    url = f"https://trefle.io/api/v1/plants?filter[scientific_name]={scientific_name}&token={TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {scientific_name}: {e}")
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
    plant_info = {
        'common_name': plant_data.get('common_name', 'Unknown'),
        'scientific_name': plant_data.get('scientific_name'),
        'year': plant_data.get('year'),
        'genus_id': plant_data.get('genus_id'),
        'family': plant_data.get('family'),
        'genus': plant_data.get('genus'),
    }

    if not plant_info.get('scientific_name'):
        print(f"Skipping: No scientific name for {plant_info.get('common_name')}")
        return False

    field_mapping = {
        'growth_rate': 'growth_rate',
        'maximum_height': 'max_height',
        'average_height': 'avg_height',
        'growth_months': 'growth_months',
        'row_spacing': 'row_spacing',
        'spread': 'spread',
        'toxicity': 'toxicity',
        'soil_humidity': 'soil_moisture',
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
        'ligneous_type': 'ligneous_type',
        'vegetable': 'vegetable',
        'edible': 'edible',
        'edible_parts': 'edible_parts',
    }

    for api_field, model_field in field_mapping.items():
        value = detailed_data.get(api_field)
        if value is not None:
            plant_info[model_field] = value
            print(f" Set {model_field} = {value}")

    nested_fields = {
        'minimum_precipitation': ('min_precipitation', 'mm'),
        'maximum_precipitation': ('max_precipitation', 'mm'),
        'minimum_temperature': ('min_temp', 'deg_c'),
        'maximum_temperature': ('max_temp', 'deg_c'),
        'minimum_root_depth': ('min_root_depth', 'cm'),
    }

    for api_field, (model_field, subkey) in nested_fields.items():
        nested = detailed_data.get(api_field)
        if isinstance(nested, dict) and subkey in nested:
            plant_info[model_field] = nested[subkey]
            print(f"  ↳ Set {model_field} = {nested[subkey]} (from {api_field}.{subkey})")

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

    for scientific_name in PLANTS_TO_FETCH:
        print(f"\nSearching for: {scientific_name}")
        plants = fetch_plant_by_name(scientific_name)

        if not plants:
            print(f"No results found for '{scientific_name}'")
            continue

        plant = plants[0]
        plants_processed += 1

        detailed_data = None
        self_link = plant.get('links', {}).get('self')
        if not self_link:
            print(f"No self link found for {scientific_name}. Skipping.")
            continue
        if self_link:
            print("Fetching detailed information...")
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

if __name__ == "__main__":
    fetch_and_save_plants()
