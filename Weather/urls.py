from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.get),
    path('city/',views.post),
    path('cityip/',views.post_using_ip),
    ]
