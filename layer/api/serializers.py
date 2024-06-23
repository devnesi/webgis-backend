from rest_framework.serializers import ModelSerializer, IntegerField, Serializer
from layer.models import Layer

class LayerSerializer(ModelSerializer):
    class Meta:
        model = Layer
        fields = '__all__'

class OrderSerializer(Serializer):
    id_layer = IntegerField()
    order = IntegerField()

class OrdersPayloadSerializer(Serializer):
    orders = OrderSerializer(many=True)