from rest_framework.serializers import ModelSerializer
from form.models import Form

class FormSerializer(ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        
