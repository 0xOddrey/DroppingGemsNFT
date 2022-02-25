from rest_framework import serializers
from .models import gemsMeta

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = gemsMeta
        fields = ['name', 'description', 'image']