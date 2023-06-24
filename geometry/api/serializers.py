from rest_framework.serializers import ModelSerializer
from geometry.models import Geometry

class GeometrySerializer(ModelSerializer):
    class Meta:
        model = Geometry
        fields = '__all__'
        