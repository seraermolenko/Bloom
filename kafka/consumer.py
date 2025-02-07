from kafka import KafkaConsumer
import json

# NOTE: Kafka stores messages in a binary format, not as a string. Need to deserialize

consumer = KafkaConsumer(
    "humidity",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="humidity-group",
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Listening for humidity data...")
for message in consumer:
    data = message.value
    print(f"Received data from {data['plant_id']}: {data['humidity']}% humidity")