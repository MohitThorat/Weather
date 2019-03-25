from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.get,name = 'get'),
    path('city/',views.post),
    path('cityip/',views.post_using_ip),
    path('forecast/',views.homeforecast,name = 'homeforecast'),
    path('getforecast/',views.getforecast),
    path('getforecastip/',views.getforecastip),
    ]
