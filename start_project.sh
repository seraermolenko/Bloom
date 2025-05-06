#!/bin/zsh


echo "Starting Kafka (KRaft mode)..."
kafka-server-start /opt/homebrew/etc/kafka/kraft/server.properties &
sleep 5 

echo "Activating virtual environment..."
source myenv/bin/activate

echo "Starting Django backend (Daphne ASGI)..."
daphne bloom.asgi:application &

echo "Starting Kafka consumer (moisture)..."
PYTHONPATH=. DJANGO_SETTINGS_MODULE=bloom.settings python kafka/consumer_moisture.py &

echo "Starting React frontend..."
cd bloom-frontend && npm run dev &
cd ..

echo "Project started! Check running processes in other terminals if needed."
