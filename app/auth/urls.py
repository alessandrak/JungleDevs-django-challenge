from django.urls import path, include

from rest_framework import routers

from . import views


urlpatterns = [
    path('api/login/', views.LoginAPIView.as_view(), name='login'),
    path('api/sign-up/', views.SignUpCreateAPIView.as_view(), name='sign-up'),
]