from django.shortcuts import render
from rest_framework import viewsets
from ..bloom.models import Gardens
from .serializers import GardensSerializer
from rest_framework import viewsets
from .models import Plant
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  
from .models import personalPlant
from .serializers import PlantSerializer
from .serializers import personalPlantSerializer

def home(request):
    return render(request, 'home.html') 

class GardensViewSet(viewsets.ModelViewSet):
    queryset = Gardens.objects.all()
    serializer_class = GardensSerializer

@api_view(['GET'])
def search_plants(request):
    query = request.GET.get('name')
    
    plants = Plant.objects.filter(
    Q(common_name__icontains=query) | Q(scientific_name__icontains=query) )

    if not plants:
        return Response('No plants found', status=status.HTTP_404_NOT_FOUND)
    
    serializer = PlantSerializer(plants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)