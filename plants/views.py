from rest_framework import viewsets
from .models import Plant
from .models import personalPlant
from .serializers import PlantSerializer
from .serializers import personalPlantSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = personalPlant.objects.all()
    serializer_class = personalPlantSerializer