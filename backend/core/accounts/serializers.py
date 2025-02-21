from rest_framework import serializers
from django.contrib.auth.models import User

class registerserializers(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)  # Field for password confirmation
    email = serializers.EmailField(required=True)      # Ensure email is required

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmPassword']

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError({"confirmPassword": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Remove password2 from the validated data as it is not a User model field
        validated_data.pop('confirmPassword')
        
        # Use User.objects.create_user to create the user and hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # Only include fields you want to expose

