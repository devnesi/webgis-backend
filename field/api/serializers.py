from rest_framework.serializers import ModelSerializer
from field.models import Field

class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']