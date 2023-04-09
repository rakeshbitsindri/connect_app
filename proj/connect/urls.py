from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('connect/', views.connect, name='connect'),
    path('arista_data/', views.arista_data, name='arista_data'),
    path('add_device/', views.add_device, name='add_device'),
]
