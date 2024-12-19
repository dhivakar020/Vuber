from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ride
from .serializers import RideSerializer
import json
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .models import User
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer


@api_view(['POST'])
def request_ride(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"Received data: {data}")  # Debug: print the incoming request data

        # Create the ride or process it as needed
        # Make sure we don't pass 'id' explicitly
        if 'id' in data:
            del data['id']  # Remove 'id' if present

        serializer = RideSerializer(data=data)
        if serializer.is_valid():
            ride = serializer.save(status='requested')
            return JsonResponse({'success': True, 'ride_id': ride.id})
        else:
            print(f"Validation errors: {serializer.errors}")  # Debug: print validation errors
            return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

def rider_interface(request):
    return render(request, 'rides/map.html')


@api_view(['POST'])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Create the user

        # Generate JWT token upon signup
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User created successfully!',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate the user
        user = authenticate(request, username=email, password=password)  # Email is treated as username here
        if user:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            role_redirect_url = '/rider-dashboard/' if user.role == 'rider' else '/driver-dashboard/'

            return Response({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role,
                'redirect_url': role_redirect_url,
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def login_page(request):
    return render(request, 'rides/login.html')

@api_view(['GET'])
def signup_page(request):
    return render(request, 'rides/register.html')

@api_view(['GET'])
def rider_dashboard(request):
    return render(request, 'rides/rider_page.html')

@api_view(['GET'])
def driver_dashboard(request):
    return render(request, 'rides/driver_page.html')