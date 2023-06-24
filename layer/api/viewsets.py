from rest_framework.viewsets import ModelViewSet
from layer.api.serializers import LayerSerializer
from layer.models import Layer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from map.models import Map
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

class LayerViewSet(ModelViewSet):
    serializer_class = LayerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['map']
    enabled_methods = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Layer.objects.filter(map__user=self.request.user)

    def create(self, request):
        get_object_or_404(Map, pk=request.data['map'], user=request.user)
        return super().create(request)  
    
    def update(self, request, *args, **kwargs):
        layer = get_object_or_404(Layer, pk=kwargs['pk'], map__user=request.user)
        request.data['map'] = layer.map.pk
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):   
        return super().destroy(request, *args, **kwargs)

        