from django.contrib.gis.db import models
from layer.models import Layer
# Create your models here.


class Geometry(models.Model):
    class GeometryType(models.TextChoices):
        POLYGON = 'PL', ('POLYGON')
        POINT = 'PO', ('POINT')
        LINE = 'LN', ('LINE')
        GEOM = 'GE', ('GEOMETRY')
        
    id_geometry = models.AutoField(primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    geom = models.GeometryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    
    class Meta:
        managed = True
        db_table = 'maps_layers_geometries'
        ordering = ['pk']
        verbose_name_plural = 'Geometries'