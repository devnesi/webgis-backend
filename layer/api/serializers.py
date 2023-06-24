from rest_framework.serializers import ModelSerializer
from layer.models import Layer

class LayerSerializer(ModelSerializer):
    class Meta:
        model = Layer
        fields = '__all__'
        