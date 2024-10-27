from rest_framework.viewsets import ModelViewSet
from layer.api.serializers import LayerSerializer, OrdersPayloadSerializer
from layer.models import Layer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from map.models import Map
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import connection
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import action

class LayerViewSet(ModelViewSet):
    serializer_class = LayerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['map']
    enabled_methods = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action == 'list' or self.action == 'getBbox':
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
        map = get_object_or_404(Map, pk=request.data['map'], user=request.user)

        lastLayer = Layer.objects.filter(map=map).order_by('-order').first()
        if(lastLayer is not None):
            request.data['order'] = lastLayer.order + 1
        else:  
            request.data['order'] = 1
            
        return  super().create(request)  
    
    def update(self, request, *args, **kwargs):
        layer = get_object_or_404(Layer, pk=kwargs['pk'], map__user=request.user)
        request.data['map'] = layer.map.pk
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):   
        return super().destroy(request, *args, **kwargs)

    @action(methods=['GET'], detail=True, url_path='bbox')
    def getBbox(self, request, pk):
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT ST_Extent(geom) AS bbox FROM maps_layers_geometries where layer_id  = {pk};".format(pk=pk))
            row = cursor.fetchone()
            result = row[0]

        return JsonResponse({"bbox":result})

    @action(methods=['POST'], detail=False, url_path='updateOrder')
    def updateOrder(self, request):
        serializer = OrdersPayloadSerializer(data=request.data)
        if serializer.is_valid():
            orders = serializer.validated_data['orders']
            for order in orders:
                id_layer = order['id_layer']
                layer_order = order['order']
                
                layer = get_object_or_404(Layer, id_layer=id_layer)
                layer.order = layer_order
                layer.save()
            return JsonResponse({'status': 'orders processed'})
        return HttpResponseBadRequest()
        