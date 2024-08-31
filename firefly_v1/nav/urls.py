from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('nav', views.navigate, name='nav'),
    path('simulate', views.simulate, name='simulate'),
    path('building', views.get_building, name='building'),
]