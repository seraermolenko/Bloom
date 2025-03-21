# from kafka import KafkaConsumer
from quixstreams import Application 
import json
import requests 
from dotenv import load_dotenv
import os
import time
from confluent_kafka import TopicPartition

load_dotenv() 

broker_url = os.getenv('BROKER_URL')
humidity_url = os.getenv("HUM_URL")

def main():
    # quixstreams setup
    app = Application(
        broker_address=broker_url,
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
            # breakpoint()
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
                key = msg.key().decode('utf8')
                # json 
                value = json.loads(msg.value())
                offset = msg.offset()

                print(f"Offset: {offset}, Sensor ID: {key}, Data: {value}")
                consumer.store_offsets(msg)
                last_message_time = time.time()
                # breakpoint()

                # data = {
                #     "sensor_id": value,
                #     "humidity": key,
                # }
                # response = requests.post(humidity_url, json=data)

if __name__ == "__main__": 
    try: 
        main()
    except KeyboardInterrupt: 
        pass