from django.db import models
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
    
    class Meta:
        managed = True
        db_table = 'maps_layers_geometrys'
        ordering = ['pk']