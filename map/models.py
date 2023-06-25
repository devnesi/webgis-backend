from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Map(models.Model):
    id_map = models.AutoField(primary_key=True)
    name = models.CharField(max_length=3000, default='Unnamed map')
    enabled = models.BooleanField(blank=False, null=False, default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'maps'
        ordering = ['pk']

    def __str__(self):
        return self.name