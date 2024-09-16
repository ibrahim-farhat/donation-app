from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.register_donor, name='register_donor'),
    path('donate/', views.donate, name='donate'),
]
