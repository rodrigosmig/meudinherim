from django.conf.urls import url 
from django.conf.urls import include
from usuario import views

urlpatterns = [

	url(r'^$', views.cadastro, name='cadastro'),
	#url(r'^principal/', views.login, name='login'),
	
]