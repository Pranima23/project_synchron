from rest_framework import serializers
from . import models


class PositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Position
        fields = ['url', 'position_name']