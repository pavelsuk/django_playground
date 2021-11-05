from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hopla', views.hopla, name='hopla'),
    path('lopla', views.hopla, name='lopla'),
]
