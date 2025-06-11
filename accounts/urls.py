from django.urls import path
from .views import signup_view, login_view, dashboard_view, update_profile_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('update-profile/', update_profile_view, name='update_profile'),
]
