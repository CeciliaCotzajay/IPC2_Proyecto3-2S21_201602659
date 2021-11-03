"""Servicio1_Frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ********************************************
#  AQUI SE AÑADEN LAS URL´s YA NO EN EL OTRO
# ********************************************

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('Principal/', views.Principal, name='Principal'),
    path('acercaDe/', views.acercaDe, name='acercaDe'),
    path('recibirXML', views.recibirXML, name='recibirXML'),
    path('resetear', views.resetear, name='resetear'),
    path('enviarXML', views.enviarXML, name='enviarXML'),
]
