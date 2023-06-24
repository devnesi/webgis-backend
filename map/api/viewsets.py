from rest_framework.viewsets import ModelViewSet
from map.api.serializers import MapSerializer
from map.models import Map


class MapViewSet(ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer