from django.conf.urls import url
from django.conf.urls import include
from relatorio import views

urlpatterns = [    
    url(r'^contas_a_pagar/', views.relatorioAPagar, name='contas_a_pagar'),
    url(r'^contas_a_receber/', views.relatorioAReceber, name='contas_a_receber'),
]