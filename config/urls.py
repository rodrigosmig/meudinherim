from django.conf.urls import url
from django.conf.urls import include
from config import views

urlpatterns = [
    url(r'^$', views.config, name='config'),
    url(r'^edit-senha/', views.editSenha, name='edit-senha'),
    url(r'^edit-foto/', views.editoFoto, name='edit-foto'),
]