from rest_framework import serializers 
from .models import Gardens
from .models import Plant 
from .models import PersonalPlant 

class PlantSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Gardens
		fields = '__all__'

class PlantSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Plant 
		fields = '__all__'
		
class personalPlantSerializer(serializers.ModelSerializer): 
	plant = PlantSerializer() 
	class Meta: 
		model = PersonalPlant 
		fields = ['user', 'plant', 'care_history']