from rest_framework.viewsets import ModelViewSet
from layer.api.serializers import LayerSerializer
from layer.models import Layer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from map.models import Map
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import connection
from django.http import HttpResponse
from rest_framework.decorators import action

class LayerViewSet(ModelViewSet):
    serializer_class = LayerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['map']
    enabled_methods = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        map_id = self.request.query_params.get('map', None)
        if map_id:
            return Layer.objects.filter(map_id=map_id)
        elif self.request.user.is_authenticated:
            return Layer.objects.filter(map__user=self.request.user)
        else:
            return Layer.objects.none()

    def create(self, request):
        get_object_or_404(Map, pk=request.data['map'], user=request.user)
        return super().create(request)  
    
    def update(self, request, *args, **kwargs):
        layer = get_object_or_404(Layer, pk=kwargs['pk'], map__user=request.user)
        request.data['map'] = layer.map.pk
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

    def envelopeToSQL(self, env, pk):
        tbl = dict()
        tbl['env'] = self.envelopeToBoundsSQL(env)
        tbl['geomColumn'] = 'geom'
        tbl['table'] = 'maps_layers_geometries'
        tbl['layer'] = pk

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
                AND layer_id = {layer}
            ) 
            SELECT ST_AsMVT(mvtgeom.*) FROM mvtgeom
        """
        return sql_tmpl.format(**tbl)
    
    def queryVectorTile(self, sql):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]
    
    @action(methods=['GET'], detail=True, url_path='vectortiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).pbf', permission_classes=[], authentication_classes=[TokenAuthentication])
    def getVectorTile(self, request, pk, x ,y, z):
        get_object_or_404(Layer, pk=pk, map__user=request.user.pk)

        tile =  {   
                    'zoom':   int(z), 
                    'x':      int(x), 
                    'y':      int(y), 
                    'format': 'pbf'
                }
        
        env= self.tileToEnvelope(tile)
        sql = self.envelopeToSQL(env, pk)
        pbf = self.queryVectorTile(sql)

        return HttpResponse(content=pbf.tobytes(), content_type='application/vnd.mapbox-vector-tile')
    