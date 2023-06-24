from rest_framework.viewsets import ModelViewSet
from layer.api.serializers import LayerSerializer
from layer.models import Layer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from map.models import Map
from django.shortcuts import get_object_or_404



class LayerViewSet(ModelViewSet):
    queryset= Layer.objects.all()
    serializer_class = LayerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    enabled_methods = ['get', 'post', 'put', 'delete']

    def list(self, request):
        layers = Layer.objects.filter(map__user=request.user)
        return Response(LayerSerializer(layers, many=True).data)

    def retrieve(self, request, pk=None):
        get_object_or_404(Layer, pk=pk, map__user=request.user)
        return super().retrieve(request, pk=pk)
    
    def create(self, request):
        get_object_or_404(Map, pk=request.data['map'], user=request.user)
        return super().create(request)  
    
    def update(self, request, *args, **kwargs):
        layer = get_object_or_404(Layer, pk=kwargs['pk'], map__user=request.user)
        request.data['map'] = layer.map.pk
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):   
        get_object_or_404(Layer, pk=kwargs['pk'], map__user=request.user)
        return super().destroy(request, *args, **kwargs)

        