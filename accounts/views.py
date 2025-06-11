from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import UserSignupSerializer
from rest_framework.views import APIView
from django.conf import settings
import os


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """API endpoint for user signup."""
    data = request.data
    serializer = UserSignupSerializer(data=data)
    if serializer.is_valid():
        if get_user_model().objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email already exists.'}, status=400)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Signup successful. Redirecting to login...'
        })
    return Response({'errors': serializer.errors}, status=400)

def signup_page_view(request):
    """Render signup page or handle signup POST."""
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        serializer = UserSignupSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Signup successful. Redirecting to dashboard...")
            return redirect('dashboard')  # Redirect to dashboard after signup
        return render(request, 'accounts/signup.html', {'errors': serializer.errors})

def login_page_view(request):
    """Render login page for GET requests."""
    if request.method == 'GET':
        return render(request, 'accounts/login.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """API endpoint for user login (JWT)."""
    data = request.data
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    user = authenticate(request, email=email, password=password)

    if user:
        if user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'redirect_url': '/accounts/dashboard/',
                'message': 'Login successful. Redirecting to dashboard...'
            }, status=200)
        return Response({'error': 'Your account is inactive.'}, status=403)
    return Response({'error': 'Invalid email or password. Please check your credentials.'}, status=401)

class CustomLoginAPIView(APIView):
    """Custom API view for login with JWT."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'redirect_url': '/accounts/dashboard/',
                    'message': 'Login successful. Redirecting to dashboard...'
                }, status=200)
            return Response({'error': 'Your account is inactive.'}, status=403)
        return Response({'error': 'Invalid email or password. Please check your credentials.'}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_api_view(request):
    """JWT-protected API for user dashboard data."""
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'profile_picture': user.profile_picture.url if user.profile_picture else None
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile_api_view(request):
    """JWT-protected API for updating user profile."""
    user = request.user
    data = request.data

    new_username = data.get('username', '').strip() or user.username
    new_phone = data.get('phone_number', '').strip() or user.phone_number

    # Only check for username uniqueness if changed
    if new_username != user.username:
        from .models import Users
        if Users.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            return Response({'detail': 'This username is already taken.'}, status=400)
        user.username = new_username

    user.phone_number = new_phone

    if 'profile_picture' in request.FILES and request.FILES['profile_picture']:
        # Delete old file if exists
        if user.profile_picture and hasattr(user.profile_picture, 'path') and os.path.isfile(user.profile_picture.path):
            try:
                os.remove(user.profile_picture.path)
            except Exception:
                pass

        # Rename new file
        uploaded_file = request.FILES['profile_picture']
        ext = os.path.splitext(uploaded_file.name)[1] or ".jpg"
        new_filename = f"user_{user.pk}{ext}"
        uploaded_file.name = new_filename
        user.profile_picture = uploaded_file

    user.save()
    return Response({
        'message': 'Profile updated successfully.',
        'username': user.username,
        'phone_number': user.phone_number,
        'profile_picture': user.profile_picture.url if user.profile_picture else None
    }, status=status.HTTP_200_OK)

def dashboard_view(request):
    """Render dashboard page (data loaded via JWT API)."""
    return render(request, 'accounts/dashboard.html')

def update_profile_view(request):
    """Render update profile page (actual update should be via JWT API)."""
    return render(request, 'accounts/update_profile.html')

def index_view(request):
    """Landing page view."""
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to dashboard if logged in
    return render(request, 'accounts/index.html')  # Render index page
