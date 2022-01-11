from django.contrib import admin
from django.urls import path

from .import views
app_name = 'Story_App'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:slug>', views.post, name='Post'),
    path('like/', views.like, name='like'),
    path('join/', views.signupHandle, name='join'),
    path('login/', views.loginHandle, name='login'),
    path('logout/', views.logoutHandle, name='logout'),
    path('search/', views.search, name='search'),


]
