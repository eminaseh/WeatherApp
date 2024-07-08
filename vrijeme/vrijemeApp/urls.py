from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='naslovna'),
    path('gradovi/', views.gradovi, name='gradovi'),
    path('prijava/', views.prijava, name='prijava'),
    path('odjava/', views.odjava, name='odjava'),
    path('registracija/', views.registracija, name='registracija'),
    path('izbrisi/<grad_naziv>/', views.izbrisi_grad, name='izbrisi_grad'),
    path('profil/', views.profil, name='profil'),

]