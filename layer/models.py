from django.db import models
from map.models import Map
# Create your models here.


class Layer(models.Model):
    class GeometryType(models.TextChoices):
        POLYGON = 'PL', ('POLYGON')
        POINT = 'PO', ('POINT')
        LINE = 'LN', ('LINE')
        GEOM = 'GE', ('GEOMETRY')
        
    id_layer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=3000, blank=True, null=True)
    enabled = models.BooleanField(blank=False, null=False, default=True)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    layer_type = models.CharField(max_length=2,choices=GeometryType.choices, default=GeometryType.GEOM)

    class Meta:
        managed = True
        db_table = 'maps_layers'
        ordering = ['pk']