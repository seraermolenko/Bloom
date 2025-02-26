from rest_framework import serializers 
from .models import Gardens
from .models import Plant 
from .models import PersonalPlant 

class GardenSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Gardens
		fields = '__all__'

class PlantSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Plant 
		fields = fields = ['id', 'scientific_name', 'common_name'] 
		
class PersonalPlantSerializer(serializers.ModelSerializer): 
	plant = PlantSerializer() 
	class Meta: 
		model = PersonalPlant 
		fields = '__all__'