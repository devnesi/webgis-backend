from rest_framework.viewsets import ModelViewSet
from map.api.serializers import MapSerializer
from map.models import Map
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class MapViewSet(ModelViewSet):
    queryset= Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    enabled_methods = ['get']

    def list(self, request):
        maps = Map.objects.filter(user=request.user)
        serializer = MapSerializer(maps, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        get_object_or_404(Map, pk=pk, user=request.user)
        return super().retrieve(request, pk=pk)
        