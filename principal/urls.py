from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from principal import views

urlpatterns = [
    
    url(r'^$', views.home,name='home')
]