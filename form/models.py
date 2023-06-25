from django.db import models
from layer.models import Layer
# Create your models here.

class Form(models.Model):
    id_form = models.AutoField(primary_key=True)
    name = models.CharField(max_length=3000, default='Unnamed Form')
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        managed = True
        db_table = 'maps_layers_forms'
        ordering = ['pk']
    
    def __str__(self):
        return self.name