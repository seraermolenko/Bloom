"""
URL configuration for bloom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('plants/search/', views.search_plants, name='search_plants'),
    # path('users/', include('users.urls')), # user handeling to user app 
    path('moisture/', views.send_moisture_kafka, name='send_moisture_kafka'),
    path('evaluate_moisture/', views.evaluate_moisture, name='evaluate_moisture'),
    path('personal_plants/search/', views.search_PersonalPlant, name='search_PersonalPlant'), 
    path('personal_plants/create/', views.create_personalPlant, name='create_personalPlant'),
    path('personal_plants/delete/', views.delete_personalPlant, name='delete_personalPlant'),
    path('personal_plants/assign_sensorID/', views.assign_sensorID, name='assign_sensorID'),
    path('moisture/get_latest_moisture/', views.get_latest_moisture, name='get_latest_moisture'),
    path('get_user_gardens/', views.get_user_gardens, name='get_user_gardens'),
    path('get_garden/', views.get_garden, name='get_garden'),
    path('create_garden/', views.create_garden, name='create_garden'),
    path('delete_garden/', views.delete_garden, name='delete_garden'),
    path('taken_sensors/', views.taken_sensors, name='taken_sensors'),
    path('water/', views.send_water_kafka, name='send_water_kafka'),
    path('update_last_watered/', views.update_last_watered, name='update_last_watered'),
    path('assign_sensorID/', views.assign_sensorID, name='assign_sensorID'),
    path('get_plant_history/', views.get_plant_history, name='get_plant_history'),
    path('get_latest_moisture/', views.get_latest_moisture, name='get_latest_moisture'),
    path('get_watering_history/', views.get_watering_history, name='get_watering_history'),
    path('get_status_history/', views.get_status_history, name='get_status_history'),
]