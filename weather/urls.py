from django.urls import path
from .views import WeatherView

urlpatterns = [
    path('', WeatherView.as_view(), name='weather'),  #the path for our index view
]