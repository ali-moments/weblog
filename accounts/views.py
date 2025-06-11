from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Users
from .serializers import UserSignupSerializer  # Import the serializer

def signup_view(request):
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'password': request.POST.get('password', '').strip(),
            'confirm_password': request.POST.get('confirm_password', '').strip(),
            'referral_code': request.POST.get('referral_code', '').strip()  # New field for referral code
        }

        if data['password'] != data['confirm_password']:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=data['username']).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        serializer = UserSignupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')
        else:
            messages.error(request, "Error creating account: " + str(serializer.errors))
            return redirect('signup')

    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

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
