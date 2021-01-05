from django.contrib.auth import logout
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),

    #User auth
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    #API routes
    path('doctors', views.doctors, name='doctors'),
    path('patients', views.patients, name='patients'),
    path('patients/<int:id>', views.views.patient_by_id, name='patient_by_id'),
    path('diseases', views.diseases, name='diseases'),
    path('specialties', views.specialties, name='specialties'),
    path('subspecialties', views.subspecialties, name='subspecialties'),
    path('usertypes', views.views.usertypes, name='usertypes'),
    path('checkups/<int:patient_id>', views.checkup, name='checkups')
]