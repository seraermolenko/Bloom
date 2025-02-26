# from kafka import KafkaConsumer
from quixstreams import Application 
import json

def main():
    app = Application(
        broker_address="localhost:9092",
        loglevel="DEBUG",
        consumer_group="Humidity",
        auto_offset_reset="latest"
    )

    with app.get_consumer() as consumer: 
        #Topic of intrest 
        consumer.subscribe(["Humidity"])

        while True: 
            msg = consumer.poll(1)
            if msg is None: 
                print("Waiting...")
            elif msg.Error() is not None: 
                raise Exception(msg.error())
            else:
                # byte string so decdoing 
                key = msg.key().decode('utf8')
                # json 
                value = json.loads(msg.value)
                offset = msg.offset()

                print(f"{offset} {key} {value}")
                # consumer.store_offsets(msg)
                # breakpoint()

if __name__ == "__main__": 
    try: 
        main()
    except KeyboardInterrupt: 
        pass

# consumer = KafkaConsumer(
#     "humidity",
#     bootstrap_servers="localhost:9092",
#     auto_offset_reset="earliest",
#     enable_auto_commit=True,
#     group_id="humidity-group",
#     # NOTE: Kafka stores messages in a binary format, not as a string. Need to deserialize
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# print("Listening for humidity data...")
# for message in consumer:
#     data = message.value
#     print(f"Received data from {data['plant_id']}: {data['humidity']}% humidity")