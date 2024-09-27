from rest_framework import viewsets
from .models import Gardens
from .serializers import GardensSerializer

class GardensViewSet(viewsets.ModelViewSet):
    queryset = Gardens.objects.all()
    serializer_class = GardensSerializer