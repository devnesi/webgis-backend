from rest_framework.viewsets import ModelViewSet
from form.api.serializers import FormSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from form.models import Form

class FormViewSet(ModelViewSet):
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['layer']
    enabled_methods = ['get', 'post', 'put', 'delete']
   
    def get_permissions(self):       
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Form.objects.filter(layer__map__user=self.request.user)
        else:
            return Form.objects.all()

    def create(self, request):
        return super().create(request)  
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):   
        return super().destroy(request, *args, **kwargs)

   