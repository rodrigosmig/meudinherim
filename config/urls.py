from django.conf.urls import url
from django.conf.urls import include
from config import views

urlpatterns = [
    url(r'^$', views.config, name='config'),
]