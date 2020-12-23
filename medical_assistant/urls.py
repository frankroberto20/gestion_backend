from django.contrib.auth import logout
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),

    #User auth
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    #API routes\
    path('doctors', views.doctors, name='doctors'),
    path('patients', views.patients, name='patients'),
    path('diseases', views.diseases, name='diseases')
]