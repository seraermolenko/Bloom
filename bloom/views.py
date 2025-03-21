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
from .serializers import PersonalPlantSerializer
from kafka import KafkaProducer
import json

# def home(request):
#     return render(request, 'home.html') 


@api_view(['GET'])
def search_plants(request):
    try: 
        name = request.query_params.get('name')
    
        plants = Plant.objects.filter( Q(common_name__icontains=name) | Q(scientific_name__icontains=name) )
        if not plants:
            return Response('No plants found', status=status.HTTP_404_NOT_FOUND)

        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=400)


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
        sensor_id = data.get('sensor_id')
        humidity = data.get('humidity')

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


@api_view(['POST'])
def evaluate_humidity(request):
    try:

        data = json.loads(request.body)
        sensor_id = data.get('sensor_id')
        humidity = data.get('humidity')

        if not sensor_id or humidity is None:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)
    
        
        # NOTE: Plant assocation with sensor ID, manually add in for now
        # personal_plant = PersonalPlant.objects.get(sensor_id=sensor_id)
        # plant = personal_plant.plantID
        # humidity = plant.humidity  
        humidity = 10

        min_threshold = humidity - 2
        max_threshold = humidity + 2

        if humidity < min_threshold or humidity > max_threshold:
            return Response({"warning": "Humidity outside acceptable range!"}, status=200)
        else: 
            return Response({"message": "Humidity is within acceptable range."}, status=200)

    except Plant.DoesNotExist:
        return Response({"error": "Plant not found for the given sensor_id"}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def assign_sensorID(request):
    try: 
        sensor_id = request.query_params.get('sensorID')
        personalPlantID = request.query_params.get('personalPlantID')

        try:
            personal_plant = PersonalPlant.objects.get(personalPlantID=personalPlantID)
        except PersonalPlant.DoesNotExist:
            return Response({"error": "PersonalPlant with the given ID does not exist"}, status=404)
    
        personal_plant.sensor_id = sensor_id
        personal_plant.save()

        return Response({"message": "Sensor ID assigned successfully!"}, status=200)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=400)
    

@api_view(['GET'])
def search_PersonalPlant(request):
    try: 
        user_id = request.query_params.get('user_id')
        name = request.query_params.get('name')

        if not name:
            return Response({"error": "Name parameter is required."}, status=400)
        if not user_id:
            return Response({"error": "User_id parameter is required."}, status=400)

        personal_plants = PersonalPlant.objects.filter(name__icontains=name, user_id=user_id)
        serializer = PersonalPlantSerializer(personal_plants, many=True)
        return Response(serializer.data, status=200)
    
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def create_personalPlant(request):
    try: 
        data = json.loads(request.body)
        plant_id = data.get('plant_id')
        user_id = data.get('user_id')
        name = data.get('name')

        try:
            plant = Plant.objects.get(plant_id=plant_id)
        except plant.DoesNotExist:
            return Response({"error": "Plant with the given ID does not exist"}, status=404)

        personal_plant = PersonalPlant(
            plant_id=plant,  
            name=name,  
            user_id=user_id  
        )
        personal_plant.save()

        return Response({"message": "New personal plant created successfully!"}, status=200)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=400)
        
        