from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from .serializers import UserSignupSerializer

@api_view(['POST'])
def signup_view(request):
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
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        serializer = UserSignupSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Signup successful. Redirecting to dashboard...")
            return redirect('dashboard')  # Redirect to dashboard after signup
        return render(request, 'accounts/signup.html', {'errors': serializer.errors})

@api_view(['POST'])
def login_view(request):
    data = request.data
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    User = get_user_model()
    user = User.objects.filter(email=email).first()

    if user and user.check_password(password):  # Validate user credentials
        if user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'redirect_url': '/accounts/dashboard/',  # Include redirect URL
                'message': 'Login successful. Redirecting to dashboard...'
            }, status=200)
        return Response({'error': 'Your account is inactive.'}, status=403)
    return Response({'error': 'Invalid email or password. Please check your credentials.'}, status=401)  # Changed to 401

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'profile_picture': user.profile_picture.url if user.profile_picture else None
    })

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('dashboard')

    return render(request, 'accounts/update_profile.html')

def index_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to dashboard if logged in
    return render(request, 'accounts/index.html')  # Render index page
