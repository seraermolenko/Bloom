import requests
from ...models import Plant
import os
import time 
from requests.exceptions import ReadTimeout
from dotenv import load_dotenv  
load_dotenv()


TOKEN = os.getenv('TREFLE_API_TOKEN')

def plant_exists(scientific_name):
    return Plant.objects.filter(scientific_name=scientific_name).exists()

popular_plants = [
    "Rose", "Tulip", "Lavender", "Basil", "Sunflower", "Aloe Vera", "Orchid", "Daffodil",
    "Mint", "Cactus", "Cherry Blossom", "Fern", "Peony", "Daisy", "Begonia", "Pansy",
    "Hibiscus", "Jasmine", "Ivy", "Petunia", "Pothos", "Marigold", "Geranium", "Palm",
    "Snake Plant", "Spider Plant", "Azalea", "Clover", "Moss", "Lilac", "Carnation",
    "Fuchsia", "Anthurium", "Camellia", "Cyclamen", "Clematis", "Hosta", "Heather",
    "Hydrangea", "Impatiens", "Chrysanthemum", "Zinnia", "Poinsettia", "Violet",
    "Foxglove", "Bleeding Heart", "Forget-me-not", "Bluebell", "Amaryllis", "Primrose",
    "Coleus", "Calendula", "Crocus", "Snapdragon", "Phlox", "Coreopsis", "Lupine",
    "Delphinium", "Ranunculus", "Aster", "Verbena", "Sedum", "Salvia", "Echinacea",
    "Sweet Pea", "Dahlia", "Calla Lily", "Freesia", "Heliotrope", "Yarrow", "Thyme",
    "Parsley", "Rosemary", "Sage", "Oregano", "Cilantro", "Chive", "Bay Laurel",
    "Chamomile", "Catnip", "Lemongrass", "Stevia", "Fennel", "Mint", "Tarragon",
    "Dill", "Borage", "Sorrel", "Artichoke", "Arugula", "Spinach", "Kale", "Collard",
    "Lettuce", "Radish", "Carrot", "Beet", "Cucumber", "Pumpkin","Monstera", "Snake Plant", "Spider Plant", "Pothos", "Philodendron", "Peace Lily",
    "Aloe Vera", "Rubber Plant", "Fiddle Leaf Fig", "ZZ Plant", "Jade Plant", "Parlor Palm",
    "Bird of Paradise", "Calathea", "Chinese Evergreen", "Dracaena", "Bamboo Palm",
    "Boston Fern", "Asparagus Fern", "Croton", "Areca Palm", "Cast Iron Plant",
    "Peperomia", "String of Pearls", "Oxalis", "Kalanchoe", "Hoya", "Schefflera",
    "Anthurium", "Dieffenbachia", "Prayer Plant", "Alocasia", "Echeveria", "Succulent",
    "Cactus", "Kentia Palm", "Umbrella Tree", "Polka Dot Plant", "Pilea", "Rex Begonia",
    "Money Tree", "Yucca", "Purple Heart", "Air Plant", "Fatsia Japonica", "Creeping Fig",
    "Fittonia", "Lipstick Plant", "Crown of Thorns", "Aglaonema", "Golden Barrel Cactus",
    "Haworthia", "String of Bananas", "Burro’s Tail", "Zebra Plant", "Ponytail Palm",
    "Christmas Cactus", "Norfolk Island Pine", "Umbrella Palm", "English Ivy",
    "Maidenhair Fern", "Bird’s Nest Fern", "Dumb Cane", "Arrowhead Plant",
    "Silver Satin Pothos", "Watermelon Peperomia", "Swiss Cheese Plant",
    "Baby Rubber Plant", "Kimberly Queen Fern", "Elephant Ear Plant", "Banana Tree",
    "Papyrus Plant", "Begonia Maculata", "Tradescantia", "Staghorn Fern", "Rosary Vine",
    "Turtle Vine", "Coffee Plant", "Chili Pepper Plant", "Purple Shamrock", "Chinese Money Plant",
    "Scindapsus", "Flamingo Flower", "Dwarf Umbrella Tree", "Coral Cactus", "Split Leaf Philodendron",
    "Heartleaf Philodendron", "Grape Ivy", "Sunset Jade", "African Violet", "Miniature Bonsai",
    "Lucky Bamboo", "Hen and Chicks", "Window Leaf Plant", "Cylindrical Snake Plant",
    "Candelabra Cactus", "Button Fern", "Paperwhite Narcissus", "Caladium", "Wax Plant",
    "Bottle Palm", "Mistletoe Cactus"
]

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
    
def populate_basic_data():
    for plant_name in popular_plants:
        print(f"Fetching data for {plant_name}...")
        plants = fetch_plant_by_name(plant_name)
        for plant in plants:

            if plant_exists(plant.get('scientific_name')):
                print(f"{plant.get('common_name')} already exists in the database. Skipping.")
                continue  

            Plant.objects.update_or_create(
                scientific_name=plant.get('scientific_name'),
                defaults={
                    "common_name": plant.get('common_name'),
                    "year": plant.get('year'),
                    "family": plant.get('family'),
                    "genus": plant.get('genus'),
                    "genus_id": plant.get('genus_id'),
                    "native": plant.get('distribution', {}).get('native'),
                    "edible": plant.get('edible'),
                    "edible_parts": plant.get('edible_part'),
                    "toxicity": plant.get('toxicity')
                }
            )
            print(f"Added {plant.get('common_name')} to the database.")
        
        time.sleep(0.5) 

populate_basic_data()
