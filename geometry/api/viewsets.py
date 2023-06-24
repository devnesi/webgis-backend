from rest_framework.viewsets import ModelViewSet
from geometry.api.serializers import GeometrySerializer
from geometry.models import Geometry
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from layer.models import Layer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

class GeometryViewSet(ModelViewSet):
    serializer_class = GeometrySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['layer']
    enabled_methods = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Geometry.objects.filter(layer__map__user=self.request.user)

    def validateGeometryType(self, typeGeometryFront, typeGeometryBack):
        return (typeGeometryFront.upper().strip() != typeGeometryBack)
    
    
    def create(self, request):
        layer = get_object_or_404(Layer, pk=request.data['layer'], map__user=request.user)

        if(self.validateGeometryType(request.data['geom']['type'], layer.layer_type)):
            return Response(status=400, data={'message': 'Invalid geometry type'})
        
        return super().create(request)  
    
    def update(self, request, *args, **kwargs):
        geometry = get_object_or_404(Geometry, pk=kwargs['pk'], layer__map__user=request.user)
        request.data['layer'] = geometry.layer.pk

        if(self.validateGeometryType(request.data['geom']['type'], geometry.layer.layer_type)):
            return Response(status=400, data={'message': 'Invalid geometry type'})
        
        return super().update(request, *args, **kwargs)
    
        