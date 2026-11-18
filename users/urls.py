from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]