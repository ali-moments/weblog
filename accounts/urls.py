from django.urls import path
from .views import signup_view, login_view, dashboard_view, signup_page_view
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse

@api_view(['GET'])
def protected_dashboard_view(request):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    return dashboard_view(request)

urlpatterns = [
    path('signup/', signup_page_view, name='signup_page'),  # Render signup page for GET
    path('api/signup/', signup_view, name='signup'),  # Handle signup API for POST
    path('login/', login_view, name='login'),  # Allow unauthenticated access
    path('dashboard/', protected_dashboard_view, name='dashboard'),  # Protected dashboard view
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
