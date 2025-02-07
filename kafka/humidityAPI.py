from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json


app = Flask(__name__)

producer = KafkaProducer(
    # kafkas contact point, the host and port of broker 
    bootstrap_servers='localhost:9092',   
 
    # Serealizer for kafka producer, converts python object to json string in UTF-8 bytes (needed for kafka sending data)
    #NOTE: Why seralizer is needed
    # Flask’s built-in request handling can automatically parse the JSON string into a Python object (like a dictionary)
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/send-humidity', methods=['POST'])
def send_humidity():
    try:
        # Reading the http post request from esp32
        data = request.json
        plant_id = data.get("sensor_id")
        humidity = data.get("humidity")

        if not plant_id or humidity is None:
            return jsonify({"error": "Missing data"}), 400

        producer.send("humidity", key=plant_id.encode(), value=data)
        return jsonify({"message": "Data sent to Kafka"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
