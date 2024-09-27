from rest_framework import serializers 
from .models import Plant 
from .models import personalPlant 

class PlantSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Plant 
		fields = '__all__'
		
class personalPlantSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = personalPlant 
		fields = '__all__'