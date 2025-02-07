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


# # Extracts general idenficiaions  
# def extract_plant_basic(plants):
#     for plant in plants: 
#         common_name=plant.get('common_name')
#         if not common_name:
#                 common_name = "Unknown" 

#         Plant.objects.update_or_create( 
#             common_name=common_name,
#             scientific_name=plant.get('scientific_name'),                           # Has to have scientific name at minimum to be added 
#             year=plant.get('year'),
#             genus_id=plant.get('genus_id'),
#             family=plant.get('family'),
#             genus=plant.get('genus'),
#         )

# # Extracts plants self link for detailed data
# def get_plant_self_link(self_link):
#     url = f'https://trefle.io{self_link}'
#     headers = {
#         'Authorization': f'Bearer {TOKEN}'
#     }
#     response = requests.get(url, headers=headers)

# # Extracts detailed idenficiaions 
# def extract_plant_detailed(plants):
#     keys = ['shape_and_orientation', 'edible', 'edible_part', 'duration', 'observation', 'vegetable', 
#         'leaf_retention', 'texture', 'conspicuous', 'shape', 'color', 'growth_rate', 'maximum_height', 
#         'avg_height', 'toxicity', 'soil_humidity', 'soil_texture', 'soil_nutriments', 'soil_salinity', 
#         'ph_maximum', 'ph_minimum', 'light', 'maximum_temperature', 'minimum_temperature', 
#         'minimum_root_depth', 'spread', 'row_spacing', 'days_to_harvest', 'atmospheric_humidity', 
#         'maximum_precipitation', 'minimum_precipitation', 'bloom_months', 'fruit_months', 
#         'ligneous_type']

#     for plant in plants:
#         self_link = plant.get('links', {}).get('self')     
#         if self_link:
#             detailed_plant_data = get_plant_self_link(self_link)

#             data = {key: detailed_plant_data.get(key) for key in keys}            
#             Plant.objects.update_or_create(**data)                                      # ** unpacks data dictionary of key-value pairs
            
# # Loadinf the last saved page
# def last_page():
#     if os.path.exists('page.txt'):
#         with open('page.txt', 'r') as f:                                                # Proerlly opening and closing with 'with'
#             return int(f.read())
#     return 1                                                                            # If no file exsits 

# # Main Api call for Plant propogation 
# def fetch_plant_data():
#     url = 'https://trefle.io/api/v1/plants'
#     params = {
#         'token': TOKEN, 
#         'page': last_page()
#     }

#     plants = []
#     current_page = last_page()

#     while True: 
#         print(f"Fetching page {current_page}...")  
#         retries = 0
#         while retries < 3:
#             try:
#                 response = requests.get(url, params=params, timeout=10)                 # Time out is 10s
#                 if response.status_code != 200:
#                     print(f"Error: {response.status_code}")
#                     print(f"Response: {response.text}")
#                     break

#                 data = response.json()
#                 returned = data.get('data', [])                                         # Accessing under the 'data' key
#                 plants.extend(returned)

#                 print(f"Number of plants returned: {len(returned)}") 
#                 if len(returned) < 20:                                                  # API request returns 20 items per page 
#                     break                                                               # Stops when the last page is reached

#                 current_page += 1
#                 print(f"current page: {current_page}")
#                 with open('page.txt', 'w') as f:
#                     f.write(str(current_page))
#                 params['page'] = current_page
#                 time.sleep(0.5)                                                          # Sleep between API calls for rate limiting     
            
#             except ReadTimeout:
#                 retries += 1
#                 print(f"Request timed out for page {current_page}. Retrying {retries}/{3}...")
#                 time.sleep(2) 
                
#         if retries == 3:
#             print(f"Max retries reached for page {current_page}. Moving to the next page...")
#             with open('error_pages.txt', 'w') as f:
#                 f.write(str(current_page))
#             break

#     print(f"Total plants fetched: {len(plants)}")   
#     extract_plant_basic(plants)
#     #extract_plant_detailed(plants)

# fetch_plant_data()


