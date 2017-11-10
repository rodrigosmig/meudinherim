from django.conf.urls import url
from django.conf.urls import include
from contas_a_pagar import views

urlpatterns = [    
    url(r'^$', views.contasAPagar, name='index'),
    url(r'^edit/', views.editContasPagar, name='edit'),
    url(r'^delete/', views.delContasPagar, name='delete'),
    url(r'^banco/', views.banco, name='banco'),
    url(r'^pagar/', views.pagamento, name='pagar'),
]