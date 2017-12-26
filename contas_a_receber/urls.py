from django.conf.urls import url
from django.conf.urls import include
from contas_a_receber import views

urlpatterns = [    
    url(r'^$', views.contasAReceber, name='index'),
    url(r'^edit/', views.editContasReceber, name='edit'),
    url(r'^delete/', views.delContasReceber, name='delete'),
    url(r'^receber/', views.recebimento, name='receber'),
    url(r'^cancelar/', views.cancelaRecebimento, name='cancelar'),
    url(r'^verificar/', views.verificarRecebimento, name='verificar'),
]