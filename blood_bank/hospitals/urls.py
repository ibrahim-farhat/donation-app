from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.register_hospital, name='register_hospital'),
    path('request/', views.request, name='request'), 
    path('request_list/', views.request_list, name='request_list'),
]
