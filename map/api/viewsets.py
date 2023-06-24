from rest_framework.viewsets import ModelViewSet
from map.api.serializers import MapSerializer
from map.models import Map
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import connection
from django.http import HttpResponse


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
        