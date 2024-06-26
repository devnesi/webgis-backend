from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from map.api.viewsets import MapViewSet
from layer.api.viewsets import LayerViewSet
from geometry.api.viewsets import GeometryViewSet
from user.api.viewsets import UserViewSet
from form.api.viewsets import FormViewSet
from field.api.viewsets import FieldViewSet
from rest_framework.authtoken import views
if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()


router.register(r'maps', MapViewSet, basename='maps') 
router.register(r'layers', LayerViewSet, basename='layers')
router.register(r'geometries', GeometryViewSet, basename='geometries')
router.register(r'forms', FormViewSet, basename='forms')
router.register(r'fields',FieldViewSet, basename='fields')
router.register(r'register', UserViewSet, basename='register')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', views.obtain_auth_token)
]
