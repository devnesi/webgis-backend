from django.db import models
from field.models import Field
from geometry.models import Geometry

# Create your models here.

class Value(models.Model):       
    id_value = models.AutoField(primary_key=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)  
    geometry = models.ForeignKey(Geometry, on_delete=models.CASCADE)  
    string_value = models.CharField(max_length=3000, null=True, blank=True)
    number_value = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    
    class Meta:
        managed = True
        db_table = 'maps_layers_forms_fields_values'
        ordering = ['pk']
