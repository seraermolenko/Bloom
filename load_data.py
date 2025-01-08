import requests
from .plants.models import Plant
import os
import time 
from requests.exceptions import ReadTimeout
from dotenv import load_dotenv  
load_dotenv()

TOKEN = os.getenv('TREFLE_API_TOKEN')

# Extracts general idenficiaions  
def extract_plant_basic(plants):
    for plant in plants: 
        common_name=plant.get('common_name')
        if not common_name:
                common_name = "Unknown" 

        Plant.objects.update_or_create( 
            common_name=common_name,
            scientific_name=plant.get('scientific_name'),                           # Has to have scientific name at minimum to be added 
            year=plant.get('year'),
            genus_id=plant.get('genus_id'),
            family=plant.get('family'),
            genus=plant.get('genus'),
        )

# Extracts plants self link for detailed data
def get_plant_self_link(self_link):
    url = f'https://trefle.io{self_link}'
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    response = requests.get(url, headers=headers)

# Extracts detailed idenficiaions 
def extract_plant_detailed(plants):
    keys = ['shape_and_orientation', 'edible', 'edible_part', 'duration', 'observation', 'vegetable', 
        'leaf_retention', 'texture', 'conspicuous', 'shape', 'color', 'growth_rate', 'maximum_height', 
        'avg_height', 'toxicity', 'soil_humidity', 'soil_texture', 'soil_nutriments', 'soil_salinity', 
        'ph_maximum', 'ph_minimum', 'light', 'maximum_temperature', 'minimum_temperature', 
        'minimum_root_depth', 'spread', 'row_spacing', 'days_to_harvest', 'atmospheric_humidity', 
        'maximum_precipitation', 'minimum_precipitation', 'bloom_months', 'fruit_months', 
        'ligneous_type']

    for plant in plants:
        self_link = plant.get('links', {}).get('self')     
        if self_link:
            detailed_plant_data = get_plant_self_link(self_link)

            data = {key: detailed_plant_data.get(key) for key in keys}            
            Plant.objects.update_or_create(**data)                                      # ** unpacks data dictionary of key-value pairs
            
# Loadinf the last saved page
def last_page():
    if os.path.exists('page.txt'):
        with open('page.txt', 'r') as f:                                                # Proerlly opening and closing with 'with'
            return int(f.read())
    return 1                                                                            # If no file exsits 

# Main Api call for Plant propogation 
def fetch_plant_data():
    url = 'https://trefle.io/api/v1/plants'
    params = {
        'token': TOKEN, 
        'page': last_page()
    }

    plants = []
    current_page = last_page()

    while True: 
        print(f"Fetching page {current_page}...")  
        retries = 0
        while retries < 3:
            try:
                response = requests.get(url, params=params, timeout=10)                 # Time out is 10s
                if response.status_code != 200:
                    print(f"Error: {response.status_code}")
                    print(f"Response: {response.text}")
                    break

                data = response.json()
                returned = data.get('data', [])                                         # Accessing under the 'data' key
                plants.extend(returned)

                print(f"Number of plants returned: {len(returned)}") 
                if len(returned) < 20:                                                  # API request returns 20 items per page 
                    break                                                               # Stops when the last page is reached

                current_page += 1
                print(f"current page: {current_page}")
                with open('page.txt', 'w') as f:
                    f.write(str(current_page))
                params['page'] = current_page
                time.sleep(0.5)                                                          # Sleep between API calls for rate limiting     
            
            except ReadTimeout:
                retries += 1
                print(f"Request timed out for page {current_page}. Retrying {retries}/{3}...")
                time.sleep(2) 
                
        if retries == 3:
            print(f"Max retries reached for page {current_page}. Moving to the next page...")
            with open('error_pages.txt', 'w') as f:
                f.write(str(current_page))
            break

    print(f"Total plants fetched: {len(plants)}")   
    extract_plant_basic(plants)
    #extract_plant_detailed(plants)

fetch_plant_data()


