from django.urls import path, include
from . import views


urlpatterns = [
     path('', views.home, name="ospapp-home"),
     path('about/', views.about, name="ospapp-about"),
]
