from django.core.management.base import BaseCommand
from quixstreams import Application
from kafka import KafkaConsumer
import json
import requests
from dotenv import load_dotenv
import os
import time
from confluent_kafka import TopicPartition

# Load environment variables
load_dotenv()

broker_url = os.getenv('BROKER_URL')
moisture_url = os.getenv("MOIST_URL")

class Command(BaseCommand):
    help = "Start Kafka consumer to process messages"

    def handle(self, *args, **options):
        self.stdout.write("Consumer starting...")

        # QuixStreams setup
        app = Application(
            broker_address=broker_url,
            loglevel="DEBUG",
            auto_offset_reset="earliest",
        )

        self.stdout.write("Subscribed to humidity topic...")

        with app.get_consumer() as consumer:
            # Topic of interest
            consumer.subscribe(["humidity"])

            last_message_time = time.time()
            last_reset_time = time.time()

            while True:
                msg = consumer.poll(5)  # 5-second timeout
                if msg is None:
                    self.stdout.write("Waiting...")
                    current_time = time.time()

                    # Check if it's been 24 hours with no messages
                    if current_time - last_reset_time > 86400 and current_time - last_message_time > 5:
                        self.stdout.write("No messages received, resetting offset to 0...")
                        partitions = consumer.assignment()

                        # Seek to the beginning of each partition
                        for partition in partitions:
                            consumer.seek(TopicPartition(partition.topic, partition.partition, 0))
                        self.stdout.write("Offset reset to beginning")
                        last_reset_time = current_time
                        last_message_time = current_time

                elif msg.error() is not None:
                    raise Exception(msg.error())
                else:
                    # Decode message
                    self.stdout.write(f"Received message: {msg.value()}")
                    key = msg.key().decode('utf8')
                    value = json.loads(msg.value())
                    offset = msg.offset()

                    self.stdout.write(f"Offset: {offset}, Sensor ID: {key}, Data: {value}")

                    data = {
                        "sensor_id": int(key),
                        "moisture": value['moisture'],
                    }

                    try:
                        self.stdout.write(f"Sending request to: {moisture_url} with data: {data}")
                        response = requests.post(moisture_url, json=data)
                        self.stdout.write(f"Response status: {response.status_code}")

                        if response.status_code == 200:
                            self.stdout.write(f"Successfully updated plant status: {response.json()}")
                            self.stdout.write(f"Storing offset: {msg.offset()}")
                            consumer.store_offsets(msg)
                        else:
                            self.stdout.write(f"Failed to update plant status: {response.status_code}")
                            return {"error": f"Failed to update plant status: {response.status_code}"}
                    except requests.exceptions.RequestException as e:
                        self.stdout.write(f"Error sending request: {e}")
                        return {"error": f"Request failed: {e}"}

                    last_message_time = time.time()

