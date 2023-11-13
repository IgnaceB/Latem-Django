"""
URL configuration for latem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('realisations/<str:name>/', views.description_real, name='real'),
    path('account',views.account, name='account'),
    path('contact',views.home, name='contact'),
    path('configurateur',views.home, name='configurateur'),
    path('login',views.log_in, name='login'),
    path('signup',views.signup, name='signup'),
    path('logout',views.log_out, name='logout'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('param', views.param, name='param'),
    path('devis/<int:id>/', views.devis, name='devis'),
    
]
