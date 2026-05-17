from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_api, name='test_api'),
    path('crop/', views.crop_recommendation, name='crop_recommendation'),
    path('fertilizer/', views.fertilizer_recommendation, name='fertilizer_recommendation'),
    path('pesticide/', views.pesticide_recommendation, name='pesticide_recommendation'),
    path('weather-tips/', views.weather_tips, name='weather_tips'),  # ADD THIS
]