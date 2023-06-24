from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from map.api.viewsets import MapViewSet

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()


router.register(r'maps', MapViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
