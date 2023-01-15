from django.urls import path
from . import views

urlpatterns = [
    path('', views.listaAccesos.as_view(), name="lista_puntoswifi"),
]