from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'date_joined','is_staff')
        read_only_fields = ('id', 'username', 'password', 'email', 'date_joined','is_staff')