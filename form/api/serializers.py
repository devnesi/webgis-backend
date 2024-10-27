from rest_framework.serializers import ModelSerializer, SerializerMethodField

from field.models import Field
from field.api.serializers import FieldSerializer
from form.models import Form

class FormSerializer(ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True, source='field_set') 
    class Meta:
        model = Form
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
