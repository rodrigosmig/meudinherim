from django.conf.urls import url
from django.conf.urls import include
from banco import views

urlpatterns = [    
    url(r'^$', views.banco, name='banco'),
    url(r'^agencia/', views.cadastroBanco, name='agencia'),
    url(r'^edit/', views.editLancamento, name='edit'),
    url(r'^delete/', views.delLancamento, name='delete'),
    url(r'^add/', views.addLancamento, name='add'),
   	url(r'^editag/', views.editAgencia, name='editag'),
   	url(r'^delag/', views.delAgencia, name='delag'),
   	url(r'^verificar/', views.verificarContas, name='verificar'),
    url(r'^getAgencias/', views.getAgencias, name='getAgencias'),
    url(r'^getCredito/', views.getCartao_Credito, name='getCredito'),
    url(r'^transferencia/', views.transferenciaEntreContas, name='transferencia'),
    url(r'^saque/', views.saqueBancario, name='saque'),
]