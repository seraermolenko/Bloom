from quixstreams import Application 
import json
import requests 
from dotenv import load_dotenv
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bloom.settings")
django.setup()
import time
from confluent_kafka import TopicPartition
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
import json
import time
from bloom.models import PersonalPlant 

load_dotenv() 

broker_url = os.getenv('BROKER_URL')
moisture_url = os.getenv("MOIST_URL")

channel_layer = get_channel_layer()

def main():
    # quixstreams setup
    app = Application(
        broker_address=broker_url,
        consumer_group="moisture-consumer",
        loglevel="DEBUG",
        auto_offset_reset="earliest",
    )

    print("Consumer started...")
    with app.get_consumer() as consumer: 
        #Topic of intrest 
        consumer.subscribe(["humidity"])
        print("Subscribed to topic: humidity")
        last_message_time = time.time()
        last_reset_time = time.time()

        while True: 
            msg = consumer.poll(5)  # 5 second time out 
            #breakpoint()
            if msg is None: 
                print("Waiting...")
                current_time = time.time()
                # Checking that its been 24h and there are no messages found
                if current_time - last_reset_time > 86400 and current_time - last_message_time > 5:
                    print("No messages received and 24 hours passed, resetting to offset 0...")
                
                    # Get the partition assignment
                    partitions = consumer.assignment()
                    
                    # Seek to the beginning of each partition
                    for partition in partitions:
                            consumer.seek(TopicPartition(partition.topic, partition.partition, 0))
                    print("Offset reset to beginning")
                    last_reset_time = current_time  
                    last_message_time = current_time 

            elif msg.error() is not None: 
                raise Exception(msg.error())
            else:
                # byte string so decdoing 
                print(f"Received message: {msg.value()}")
                key = msg.key().decode('utf8')
                # json 
                value = json.loads(msg.value())
                offset = msg.offset()

                print(f"Offset: {offset}, Sensor ID: {key}, Data: {value}")
                sensor_id=int(key)
                personal_plant = PersonalPlant.objects.get(sensor_id=sensor_id)

                data = {
                    "sensor_id": int(key),
                    "moisture": value['moisture'],
                    "garden_id": personal_plant.garden.id
                }

                try:
                    print(f"Sending request to: {moisture_url} with data: {data}")
                    response = requests.post(moisture_url, json=data)
                    print(f"Response status: {response.status_code}")

                    try:
                        personal_plant = PersonalPlant.objects.get(sensor_id=data["sensor_id"])
                        garden_id = personal_plant.garden.id

                        if response.status_code == 200:
                            print(f"Successfully updated plant status: {response.json()}")
                            print(f"Storing offset: {msg.offset()}")
                            consumer.store_offsets(msg)

                            garden_id = data.get("garden_id")
                            if garden_id:
                                async_to_sync(channel_layer.group_send)(
                                    f"garden_{garden_id}",  
                                    {
                                        'type': 'plant_status_update',  
                                        'updated_plant': {
                                        'sensor_id': data["sensor_id"],
                                        'status': response.json()['status'],
                                        'garden_id': garden_id,
                                        }
                                    }
                                )
                                print(f"Sent WebSocket update to group garden_{garden_id}")
                        else:
                            print(f"Failed to update plant status: {response.status_code}")
                            return {"error": f"Failed to update plant status: {response.status_code}"}
                    except PersonalPlant.DoesNotExist:
                        print("PersonalPlant not found for WebSocket broadcast.")
                except requests.exceptions.RequestException as e:
                    print(f"Error sending request: {e}")
                    return {"error": f"Request failed: {e}"}
                last_message_time = time.time()

if __name__ == "__main__": 
    try: 
        main()
    except KeyboardInterrupt: 
        pass