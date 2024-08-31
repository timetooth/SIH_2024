from . import models
from rest_framework import serializers

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Building
        fields = '__all__'