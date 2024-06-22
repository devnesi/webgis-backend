from rest_framework.viewsets import ModelViewSet
from map.api.serializers import MapSerializer
from map.models import Map
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from layer.models import Layer
from geometry.models import Geometry
from django.db import connection
from django.http import JsonResponse
import json
import shapely
import shapely.ops

class MapViewSet(ModelViewSet):
    serializer_class = MapSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    enabled_methods = ['get', 'post', 'put', 'delete']

    def get_permissions(self):       
        if self.action == 'retrieve' or self.action == 'getBbox':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        print(self.request.user.is_authenticated)
        if self.request.user.is_authenticated:
            return Map.objects.filter(user=self.request.user)
        else:
            return Map.objects.all()
    
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
   
    @action(methods=['GET'], detail=True, url_path='bbox')
    def getBbox(self, request, pk):
        get_object_or_404(Map, pk=pk)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT ST_Extent(geom) AS bbox FROM maps_layers_geometries where layer_id in (select id_layer from maps_layers ml where map_id = 3)".format(pk=pk))
            row = cursor.fetchone()
            result = row[0]

        return JsonResponse({"bbox":result})