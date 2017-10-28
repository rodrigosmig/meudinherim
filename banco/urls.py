from django.conf.urls import url
from django.conf.urls import include
from banco import views

urlpatterns = [    
    url(r'^$', views.banco, name='banco'),
    url(r'^agencia/', views.cadastroBanco, name='agencia'),
]