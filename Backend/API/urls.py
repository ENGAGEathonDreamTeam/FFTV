from django.urls import path
from .views import TestAPIView, LoginAPIView, RegisterAPIView, UpdateUserAPIView

urlpatterns = [
    path('test-api/', TestAPIView.as_view(), name='test-api'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('update-user/<str:username>/', UpdateUserAPIView.as_view(), name='api_update_user'),
]
