from django.urls import path
from . import views

urlpatterns = [
    path('navigate', views.navigate, name='navigate'),
    path('test', views.test, name='test'),
]