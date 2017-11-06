from django.conf.urls import url
from django.conf.urls import include
from contas_a_pagar import views

urlpatterns = [    
    url(r'^$', views.contasAPagar, name='index'),

]