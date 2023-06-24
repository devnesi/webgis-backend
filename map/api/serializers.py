from rest_framework.serializers import ModelSerializer
from map.models import Map
class MapSerializer(ModelSerializer):
    class Meta:
        model = Map
        exclude = ['user']
        read_only_fields = ['created_at', 'updated_at']