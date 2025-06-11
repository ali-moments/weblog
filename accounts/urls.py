from django.urls import path
from .views import (
    signup_view, dashboard_view, signup_page_view, dashboard_api_view,
    CustomLoginAPIView, update_profile_view, login_page_view, update_profile_api_view
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', signup_page_view, name='signup_page'),  # Render signup page for GET
    path('api/signup/', signup_view, name='signup'),  # Handle signup API for POST
    path('login/', login_page_view, name='login_page'),  # Render login page for GET
    path('api/login/', CustomLoginAPIView.as_view(), name='custom_login_api'),  # Custom REST login API (POST)
    path('dashboard/', dashboard_view, name='dashboard'),  # HTML dashboard (session login)
    path('api/dashboard/', dashboard_api_view, name='dashboard_api'),  # JWT-protected API
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update_profile/', update_profile_view, name='update_profile'),
    path('api/update_profile/', update_profile_api_view, name='update_profile_api'),  # JWT API for profile update
]
