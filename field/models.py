from django.db import models
from form.models import Form
# Create your models here.

class Field(models.Model):
    class FieldType(models.TextChoices):
        Number = 'Number', ('Number')
        String = 'String', ('String')
        
    id_field = models.AutoField(primary_key=True)
    name = models.CharField(max_length=3000, default='Unnamed Field')
    form = models.ForeignKey(Form, on_delete=models.CASCADE)  
    type = models.CharField(max_length=6,choices=FieldType.choices, default=FieldType.String)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    
    class Meta:
        managed = True
        db_table = 'maps_layers_forms_fields'
        ordering = ['pk']
    
    def __str__(self):
        return self.name
