from rest_framework import serializers
from .models import Ride
from .models import User
from django.contrib.auth.hashers import make_password

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['pickup_lat', 'pickup_lng', 'dest_lat', 'dest_lng', 'rider_id', 'status']
    
    def create(self, validated_data):
        # Ensure you don't manually set the 'id' if it doesn't need to be set
        ride = Ride.objects.create(**validated_data)
        return ride


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'role']  # Only these fields are input by the user

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)