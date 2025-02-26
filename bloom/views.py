from django.shortcuts import render
from rest_framework import viewsets
from .models import Gardens
from rest_framework import viewsets
from .models import Plant
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  
from .models import PersonalPlant
from .serializers import PlantSerializer
from .serializers import personalPlantSerializer
from kafka import KafkaProducer
import json

def home(request):
    return render(request, 'home.html') 

# class GardensViewSet(viewsets.ModelViewSet):
#     queryset = Gardens.objects.all()
#     serializer_class = GardensSerializer

@api_view(['GET'])
def search_plants(request):
    query = request.GET.get('name')
    
    plants = Plant.objects.filter(
    Q(common_name__icontains=query) | Q(scientific_name__icontains=query) )

    if not plants:
        return Response('No plants found', status=status.HTTP_404_NOT_FOUND)
    
    serializer = PlantSerializer(plants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


producer = KafkaProducer(
    # kafkas contact point, the host and port of broker 
    bootstrap_servers='localhost:9092',   
 
    # Serealizer for kafka producer, converts python object to json string in UTF-8 bytes (needed for kafka sending data)
    #NOTE: Why seralizer is needed
    # Flask’s built-in request handling can automatically parse the JSON string into a Python object (like a dictionary)
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: str(k).encode('utf-8')
)

@api_view(['POST'])
def send_humidity_kafka(request):
    try:
        # Reading the http post request from esp32
        data = request.data
        sensor_id = data.get("sensor_id")
        humidity = data.get("humidity")

        if not sensor_id or humidity is None:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

        kafka_message = {
            "humidity": humidity
        }

        producer.send("humidity", key=sensor_id, value=kafka_message)
        # send any buffered messages
        # producer.flush() 

        return Response({"message": "Data sent to Kafka"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

