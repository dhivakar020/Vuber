from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('request-ride/', views.request_ride, name='request_ride'),
    path('map/', views.rider_interface, name='rider_interface'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('login_page/', views.login_page, name='login_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('rider-dashboard/', views.rider_dashboard, name='rider_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token
]

