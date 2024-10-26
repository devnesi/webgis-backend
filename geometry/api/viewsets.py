from rest_framework.viewsets import ModelViewSet
from geometry.api.serializers import GeometrySerializer
from geometry.models import Geometry
from form.models import Form
from field.models import Field
from value.models import Value
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from layer.models import Layer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.http import JsonResponse

class GeometryViewSet(ModelViewSet):
    serializer_class = GeometrySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['layer']
    enabled_methods = ['get', 'post', 'put', 'delete']

    def get_permissions(self):       
        if self.action == 'retrieve' or self.action == 'getValues' :
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Geometry.objects.filter(layer__map__user=self.request.user)
        else:
            return Geometry.objects.all()

    def validateGeometryType(self, typeGeometryFront, typeGeometryBack):
        return (typeGeometryFront.upper().strip() != typeGeometryBack.upper())
    
    
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
    

    @action(methods=['GET'], detail=True, url_path='values')
    def getValues(self, request, pk):
        geometry = get_object_or_404(Geometry, pk=pk)
    
        forms = Form.objects.filter(layer = geometry.layer)

        response = []
        for form in forms:            
            fields = Field.objects.filter(form=form)
            values_on_form = []
            for field in fields:
                value, created = Value.objects.get_or_create(geometry=geometry, field=field)
                
                if(created == False):
                    value.save()

                values_on_form.append({
                    "id_field": field.id_field,
                    "name": field.name,
                    "type": field.type,
                    "value_string": value.string_value,
                    "value_number": value.number_value
                })

            response.append({"id_form":form.id_form, "name":form.name, "fields_values":values_on_form})
                
             
        return JsonResponse({"forms":response})
    

    @action(methods=['POST'], detail=True, url_path='infos')
    def postValues(self, request, pk):
        geometry = get_object_or_404(Geometry, pk=pk)
        data = request.data

        for form_data in data.get('forms', []):
            form = get_object_or_404(Form, id_form=form_data['id_form'])
            for field_data in form_data.get('fields_values', []):
                field = get_object_or_404(Field, id_field=field_data['id_field'])
                value, created = Value.objects.get_or_create(geometry=geometry, field=field)
                value.string_value = field_data.get('value_string', value.string_value)
                value.number_value = field_data.get('value_number', value.number_value)
                value.save()

        return Response()
