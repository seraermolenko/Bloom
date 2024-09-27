from rest_framework import serializers 
from .models import Gardens

class PlantSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Gardens
		fields = '__all__'