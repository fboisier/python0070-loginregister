from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('registro', views.registro),
    path('login', views.login),
    path('logout', views.logout),
    path('pancho', views.pancho),
    path('horas', views.horas)
]
