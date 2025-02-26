# from kafka import KafkaConsumer
from quixstreams import Application 
import json
import requests 
from dotenv import load_dotenv
import os

load_dotenv() 

broker_url = os.getenv('BROKER_URL')
humidity_url = os.getenv("HUM_URL")

def main():
    # quixstreams setup
    app = Application(
        broker_address=broker_url,
        loglevel="DEBUG",
        auto_offset_reset="latest",
    )

    print("Consumer started...")
    with app.get_consumer() as consumer: 
        #Topic of intrest 
        consumer.subscribe(["humidity"])

        while True: 
            msg = consumer.poll(2) # Change to longer time legnth once esp32 set up
            # breakpoint()
            if msg is None: 
                print("Waiting...")
            elif msg.error() is not None: 
                raise Exception(msg.error())
            else:
                # byte string so decdoing 
                key = msg.key().decode('utf8')
                # json 
                value = json.loads(msg.value())
                offset = msg.offset()

                print(f"Offset: {offset}, Sensor ID: {key}, Data: {value}")
                # consumer.store_offsets(msg)
                # breakpoint()

                data = {
                    "sensor_id": value,
                    "humidity": key,
                }
                response = requests.post(humidity_url, json=data)

if __name__ == "__main__": 
    try: 
        main()
    except KeyboardInterrupt: 
        pass