
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', lambda x: redirect('home/')),
    path('home/', views.home, name='home'),
    path('film/', views.film, name='film'),
    path('accounts/', views.accounts, name='accounts'),
    path('manager/', views.manager, name='manager'),
]