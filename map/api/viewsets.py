from rest_framework.viewsets import ModelViewSet
from map.api.serializers import MapSerializer
from map.models import Map
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from layer.models import Layer
from geometry.models import Geometry
import json
import shapely
import shapely.ops

class MapViewSet(ModelViewSet):
    serializer_class = MapSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    enabled_methods = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Map.objects.filter(user=self.request.user)
    
    def create(self, request):
        request.data['user'] = request.user.id
        return super().create(request)  
    
    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):   
        return super().destroy(request, *args, **kwargs)

    @action(methods=['POST'], detail=True, url_path='load')
    def loadFromGeojson(self, request, pk):
        map = get_object_or_404(Map, pk=pk, user=request.user)

        file = request.FILES['file']
        geojson = json.loads(file.read())
        layer_type = geojson['features'][0]['geometry']['type'].upper()        
        
        newLayer = Layer.objects.create(map=map)
        newLayer.layer_type = layer_type
        newLayer.save()

        for geom in geojson['features']:
            
            newGeometry = Geometry.objects.create(layer=newLayer)
            
            loaded = shapely.geometry.shape(geom['geometry'])
            newGeometry.geom = shapely.ops.transform(lambda x, y, z=None: (x, y), loaded).wkt

            newGeometry.save()            
            
        return Response()
        