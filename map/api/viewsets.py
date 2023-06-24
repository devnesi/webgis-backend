from rest_framework.viewsets import ModelViewSet
from map.api.serializers import MapSerializer
from map.models import Map
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db import connection
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

    def tileToEnvelope(self, tile):
        worldMercMax = 20037508.3427892
        worldMercMin = -1 * worldMercMax
        worldMercSize = worldMercMax - worldMercMin
        worldTileSize = 2 ** tile['zoom']
        tileMercSize = worldMercSize / worldTileSize
        env = dict()
        env['xmin'] = worldMercMin + tileMercSize * tile['x']
        env['xmax'] = worldMercMin + tileMercSize * (tile['x'] + 1)
        env['ymin'] = worldMercMax - tileMercSize * (tile['y'] + 1)
        env['ymax'] = worldMercMax - tileMercSize * (tile['y'])
        return env
    
    def envelopeToBoundsSQL(self, env):
        DENSIFY_FACTOR = 4
        env['segSize'] = (env['xmax'] - env['xmin'])/DENSIFY_FACTOR
        sql_tmpl = 'ST_Segmentize(ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 3857),{segSize})'
        return sql_tmpl.format(**env)

    def envelopeToSQL(self, env):
        tbl = dict()
        tbl['env'] = self.envelopeToBoundsSQL(env)
        tbl['geomColumn'] = 'geom'
        tbl['table'] = 'maps_layers_geometries'

        sql_tmpl = """
            WITH 
            bounds AS (
                SELECT {env} AS geom, 
                       {env}::box2d AS b2d
            ),
            mvtgeom AS (
                SELECT ST_AsMVTGeom(ST_Transform(t.{geomColumn}, 3857), bounds.b2d) AS geom
                FROM {table} t, bounds
                WHERE ST_Intersects(t.{geomColumn}, ST_Transform(bounds.geom, 4326))
            ) 
            SELECT ST_AsMVT(mvtgeom.*) FROM mvtgeom
        """
        return sql_tmpl.format(**tbl)
    
    def queryVectorTile(self, sql):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]
    
    @action(methods=['GET'], detail=True, url_path='vectortiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).pbf', permission_classes=[], authentication_classes=[])
    def getVectorTile(self, request, pk, x ,y, z):
        #get_object_or_404(Map, pk=pk, user=request.user)

        tile =  {   
                    'zoom':   int(z), 
                    'x':      int(x), 
                    'y':      int(y), 
                    'format': 'pbf  '
                }
        
        env= self.tileToEnvelope(tile)
        sql = self.envelopeToSQL(env)
        pbf = self.queryVectorTile(sql)

        return HttpResponse(content=pbf.tobytes(), content_type='application/vnd.mapbox-vector-tile')
    

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
        