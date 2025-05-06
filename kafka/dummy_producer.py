import requests
import random
import time
from dotenv import load_dotenv
import os

load_dotenv() 
api_url = os.getenv('SEND_MOIST_URL')


def main():
    while True:
        moisture = random.randint(1, 70)
        sensor_id = random.randint(1,4)
        data = {
            "sensor_id": sensor_id,
            "moisture": moisture
        }
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            print(f"Data sent: {data}")
        else:
            print(f"Error sending data: {response.status_code}")
        time.sleep(5)  # every 15 min 900, 1 hour 3600 


if __name__ == "__main__": 
    try: 
        main()
    except KeyboardInterrupt: 
        pass