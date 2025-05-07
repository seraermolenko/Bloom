from django.shortcuts import render
from rest_framework import viewsets
from .models import Gardens
from rest_framework import viewsets
from .models import Plant
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  
from .models import PersonalPlant, StatusHistory, WateringHistory, Plant, Gardens
from .serializers import PlantSerializer
from .serializers import PersonalPlantSerializer
from kafka import KafkaProducer
import json
from django.contrib.auth.models import User
from django.utils import timezone

@api_view(['GET'])
def search_plants(request):
    try: 
        name = request.query_params.get('name')
        if not name:
            return Response({"error": "Name parameter is required."}, status=400)
    
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

watering_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: str(k).encode('utf-8')
)

def send_water_kafka(sensor_id, plant_id):
    kafka_message = {
        "sensor_id": sensor_id,
        "plant_id": plant_id,
    }
    try:
        watering_producer.send("water", key=sensor_id, value=kafka_message)
        watering_producer.flush()  
        print(f"Sent watering trigger to Kafka for plant {plant_id} with sensor {sensor_id}")
        return True  
    except Exception as e:
        print(f"Error sending watering message to Kafka: {e}")
        return False  

moisture_producer = KafkaProducer(
    # kafkas contact point, the host and port of broker 
    bootstrap_servers='localhost:9092',   
 
    # Serealizer for kafka producer, converts python object to json string in UTF-8 bytes (needed for kafka sending data)
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: str(k).encode('utf-8')
)

latest_moisture_readings = {}
@api_view(['POST'])
def send_moisture_kafka(request):
    try:
        # Reading the http post request from esp32
        data = request.data
        sensor_id = data.get('sensor_id')
        moisture = data.get('moisture')

        if not sensor_id or moisture is None:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

        latest_moisture_readings[str(sensor_id)] = moisture

        kafka_message = {
            "moisture": moisture
        }

        moisture_producer.send("moisture", key=sensor_id, value=kafka_message)
        # send any buffered messages
        # producer.flush() 

        return Response({"message": "Data sent to Kafka"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def evaluate_moisture(request):
    try:
        print("inside function")
        data = json.loads(request.body)
        sensor_id = data.get('sensor_id')
        moisture = data.get('moisture')

        if not sensor_id or moisture is None:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)
    
        personal_plant = PersonalPlant.objects.get(sensor_id=int(sensor_id))
        print(f"Plant found: {personal_plant.id}, Current moisture: {moisture}")  # Debugging line

        # NOTE: Plant assocation with sensor ID, manually add in for now
        # personal_plant = PersonalPlant.objects.get(sensor_id=sensor_id)
        # plant = personal_plant.plantID
        # moisture = plant.moisture  

        min_threshold = 5 #personal_plant.plant.soil_moisture - 2
        max_threshold = 30 #personal_plant.plant.soil_moisture + 2
        print(f"Moisture: {moisture}, Min Threshold: {min_threshold}, Max Threshold: {max_threshold}")
        
        previous_status = personal_plant.status

        if moisture < min_threshold:
            personal_plant.status = 'Thirsty'
            if personal_plant.auto_watering:
                print(f"Moisture below threshold, triggering watering for plant {personal_plant.id}")
                success = send_water_kafka(sensor_id, personal_plant.id)  
                if success:
                    print(f"Successfully sent message to water plant {personal_plant.id}, last watered updated.")
                else:
                    print(f"Failed to send trigger message to water the plant {personal_plant.id}, last watered not updated.")
        elif moisture > max_threshold:
            personal_plant.status = 'Wet'
        else: 
            personal_plant.status = 'Happy'

        if personal_plant.status != previous_status:
            StatusHistory.objects.create(
                personal_plant=personal_plant,
                status=personal_plant.status
            )
            print(f"Status history updated: {personal_plant.status}")

        personal_plant.save()
        print(f"Updated plant status to: {personal_plant.status} for plant {personal_plant.id}")
        return Response({"status": personal_plant.status}, status=status.HTTP_200_OK)

    except Plant.DoesNotExist:
        return Response({"error": "Plant not found for the given sensor_id"}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_last_watered(request):
    try:
        sensor_id = request.data.get('sensor_id')
        plant_id = request.data.get('plant_id')
        watering_successful = request.data.get('watering_successful')

        personal_plant = PersonalPlant.objects.get(sensor_id=sensor_id, id=plant_id)

        if watering_successful:
            personal_plant.last_watered = timezone.now()
            personal_plant.save()
            print(f"Successfully updated last watered for plant {plant_id}.")
            WateringHistory.objects.create(
                personal_plant=personal_plant,
            )
            print(f"Successfully updated last watered for plant {plant_id}.")
        else:
            print(f"Watering failed for plant {plant_id}, not updating last watered.")

        return Response({"status": "success"}, status=200)

    except PersonalPlant.DoesNotExist:
        return Response({"error": "Plant not found"}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=500)

@api_view(['PUT'])
def assign_sensorID(request):
    try: 
        sensor_id = request.query_params.get('sensor_id')
        personalPlant_id = request.query_params.get('personalPlant_id')

        try:
            personal_plant = PersonalPlant.objects.get(id=personalPlant_id)
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

        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        personal_plants = PersonalPlant.objects.filter(user=user)
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
        user = User.objects.first()  
        data = json.loads(request.body)
        plant_id = data.get('plant_id')
        custom_name = data.get('custom_name')
        sensor_id = data.get('sensor_id')
        garden_id = data.get('garden_id')
        auto_watering = data.get('auto_watering')


        try:
            plant = Plant.objects.get(id=plant_id)
        except plant.DoesNotExist:
            return Response({"error": "Plant with the given ID does not exist"}, status=404)
        try:
            garden = Gardens.objects.get(id=garden_id)
        except plant.DoesNotExist:
            return Response({"error": "Garden with the given ID does not exist"}, status=404)

        personal_plant = PersonalPlant(
            plant=plant,  
            name=custom_name,  
            user=user, 
            sensor_id=sensor_id,
            garden=garden,
            auto_watering=auto_watering,
        )
        personal_plant.save()
        return Response({"message": "New personal plant created successfully!"}, status=200)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=400)
        
        
@api_view(['GET'])
def get_latest_moisture(request):
    try:
        sensor_id = request.query_params.get('sensor_id')
        
        if not sensor_id:
            return Response({"error": "Sensor ID is required"}, status=400)
            
        moisture = latest_moisture_readings.get(str(sensor_id))
        
        if moisture is None:
            return Response({"error": "No moisture data available for this sensor"}, status=404)
            
        return Response({"sensor_id": sensor_id, "moisture": moisture}, status=200)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=400)
    

@api_view(['POST'])
def create_garden(request): 
    try: 
        data = request.data
        name = data.get('name')
        private = data.get('private', False)
        user_id = data.get('user_id')

        if not name:
            return Response({"error": "Name is required"}, status=400)
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
            
        garden = Gardens.objects.create(
            name=name,
            private=private,
            user=user,
        )
        
        return Response({
            "garden_id": garden.id,
            "user": user.username,
            "name": garden.name,
            "private": garden.private,
            "plants": [],
        }, status=201)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def get_garden(request):
    try:
        garden_id = request.query_params.get('garden_id')
        
        if not garden_id:
            return Response({"error": "Garden ID is required"}, status=400)
        
        garden = Gardens.objects.get(id=garden_id)
        personal_plants = garden.personal_plants.all() 
        print(f"Found garden: {garden.name}, with {len(personal_plants)} personal plants")
 
        plants_data = []
        for personal_plant in personal_plants:
            plant_data = PlantSerializer(personal_plant.plant).data  
            plants_data.append({
                "personal_plant_id": personal_plant.id,
                "plant_id": plant_data['id'],  
                "common_name": plant_data['common_name'],
                "custom_name": personal_plant.name,
                "sensor_id": personal_plant.sensor_id,
                "status": personal_plant.status,
                "auto_watering": personal_plant.auto_watering,
                "last_watered": personal_plant.last_watered,
                "date_added": personal_plant.date_added,
                "garden_id": personal_plant.garden.id,
                'scientific_name': personal_plant.plant.scientific_name,

                'year': personal_plant.plant.year,
                'family': personal_plant.plant.family,
                'genus': personal_plant.plant.genus,
                'genus_id': personal_plant.plant.genus_id,
                'edible': personal_plant.plant.edible,
                'edible_parts': personal_plant.plant.edible_parts,
                'vegetable': personal_plant.plant.vegetable,
                'growth_rate': personal_plant.plant.growth_rate,
                'max_height': personal_plant.plant.max_height,
                'avg_height': personal_plant.plant.avg_height,
                'growth_months': personal_plant.plant.growth_months,
                'row_spacing': personal_plant.plant.row_spacing,
                'spread': personal_plant.plant.spread,
                'toxicity': personal_plant.plant.toxicity,
                'soil_moisture': personal_plant.plant.soil_moisture,
                'soil_texture': personal_plant.plant.soil_texture,
                'soil_nutriments': personal_plant.plant.soil_nutriments,
                'soil_salinity': personal_plant.plant.soil_salinity,
                'ph_max': personal_plant.plant.ph_max,
                'ph_min': personal_plant.plant.ph_min,
                'sunlight': personal_plant.plant.sunlight,
                'max_temp': personal_plant.plant.max_temp,
                'min_temp': personal_plant.plant.min_temp,
                'days_to_harvest': personal_plant.plant.days_to_harvest,
                'atmospheric_humidity': personal_plant.plant.atmospheric_humidity,
                'min_precipitation': personal_plant.plant.min_precipitation,
                'max_precipitation': personal_plant.plant.max_precipitation,
                'min_root_depth': personal_plant.plant.min_root_depth,
                'bloom_months': personal_plant.plant.bloom_months,
                'fruit_months': personal_plant.plant.fruit_months,
                'ligneous_type': personal_plant.plant.ligneous_type,
            })

        garden_data = {
            "id": garden.id,
            "name": garden.name,
            "private": garden.private,
            "plants": plants_data,
        }
        
        return Response(garden_data)
        
    except Gardens.DoesNotExist:
        return Response({"error": "Garden not found"}, status=404)
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())  
        return Response({"error": str(e)}, status=400)
    

@api_view(['GET'])
def get_user_gardens(request):
    try:
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        
        user = User.objects.get(id=user_id)
        gardens = Gardens.objects.filter(user=user)
        
        return Response([
            {
                "garden_id": garden.id,
                "name": garden.name,
                "private": garden.private
            }
            for garden in gardens
        ])
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['DELETE'])
def delete_garden(request):
    try:
        garden_id = request.query_params.get('garden_id')
        
        if not garden_id:
            return Response({"error": "Garden ID is required"}, status=400)
        
        try:
            garden = Gardens.objects.get(id=garden_id)
        except Gardens.DoesNotExist:
            return Response({"error": "Garden not found"}, status=404)

        garden.delete()

        return Response({"message": "Garden deleted successfully"}, status=200)

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def taken_sensors(request):
    try:
        taken_sensors = PersonalPlant.objects.exclude(sensor_id=None).values('sensor_id')

        sensor_ids = [sensor['sensor_id'] for sensor in taken_sensors]

        return Response(sensor_ids, status=200)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({"error": str(e)}, status=400)
    

@api_view(['POST'])
def delete_personalPlant(request):
    try:
        personal_plant_id = request.data.get('personal_plant_id')

        if not personal_plant_id:
            return Response({"error": "Personal plant ID is required."}, status=400)

        try:
            personal_plant = PersonalPlant.objects.get(id=personal_plant_id)
        except PersonalPlant.DoesNotExist:
            return Response({"error": "Personal plant with the given ID does not exist."}, status=404)

        personal_plant.sensor_id = None
        personal_plant.save() 
        personal_plant.delete()

        return Response({"message": "Personal plant deleted successfully!"}, status=200)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def get_plant_history(request):
    try:
        plant_id = request.query_params.get('plant_id')
        personal_plant = PersonalPlant.objects.get(id=plant_id)

        status_history = personal_plant.status_history.all().values('status', 'date_changed')
        watering_history = personal_plant.watering_history.all().values('date_watered', 'watered_by')

        return Response({
            "status_history": status_history,
            "watering_history": watering_history
        })

    except PersonalPlant.DoesNotExist:
        return Response({"error": "Personal plant not found"}, status=404)


@api_view(['GET'])
def get_status_history(request):
    try:
        plant_id = request.query_params.get('plant_id')
        personal_plant = PersonalPlant.objects.get(id=plant_id)

        status_history = personal_plant.status_history.all().values('status', 'date_changed')

        return Response({
            "status_history": list(status_history)
        }, status=status.HTTP_200_OK)

    except PersonalPlant.DoesNotExist:
        return Response({"error": "Personal plant not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_watering_history(request):
    try:
        plant_id = request.query_params.get('plant_id')
        personal_plant = PersonalPlant.objects.get(id=plant_id)
        watering_history = personal_plant.watering_history.all().values('date_watered', 'watered_by')

        # Return the watering history
        return Response({
            "watering_history": list(watering_history)
        }, status=status.HTTP_200_OK)

    except PersonalPlant.DoesNotExist:
        return Response({"error": "Personal plant not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)