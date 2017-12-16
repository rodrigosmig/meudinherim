from django.conf.urls import url
from django.conf.urls import include
from caixa import views

urlpatterns = [    
    url(r'^$', views.lancamentos, name='index'),
    url(r'^categoria/', views.categoria, name='categoria'),
    url(r'^edit/', views.editLancamento, name='edit'),
    url(r'^edit-categoria/', views.editCategoria, name='edit-categoria'),
    url(r'^delete-categoria/', views.delCategoria, name='delete-categoria'),
    url(r'^delete/', views.delLancamento, name='delete'),
    url(r'^add/', views.addLancamento, name='add'),
    url(r'^verificar/', views.verificarContasAPagar, name='verificar'),
]