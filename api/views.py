from .models import *
from rest_framework import viewsets
from .serializers import *


class PositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows position of users to be viewed or edited.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer