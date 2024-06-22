from django.db import models
from map.models import Map
from django.db.models import JSONField 
# Create your models here.


class Layer(models.Model):
    class GeometryType(models.TextChoices):
        POLYGON = 'POLYGON', ('POLYGON')
        POINT = 'POINT', ('POINT')
        LINE = 'LINESTRING', ('LINESTRING')
        MULTIPOLYGON = 'MULTIPOLYGON', ('MULTIPOLYGON')
        MULTILINESTRING = 'MULTILINESTRING', ('MULTILINESTRING')
        GEOM = 'GEOM', ('GEOMETRY')
        
    id_layer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=3000, default='Unnamed Layer')
    enabled = models.BooleanField(blank=False, null=False, default=True)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    layer_type = models.CharField(max_length=15,choices=GeometryType.choices, default=GeometryType.GEOM)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    style = JSONField(default=dict)

    class Meta:
        managed = True
        db_table = 'maps_layers'
        ordering = ['pk']
    
    def __str__(self):
        return self.name