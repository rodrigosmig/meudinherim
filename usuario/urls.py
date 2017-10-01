from django.conf.urls import url 
from usuario import views

urlpatterns = [

	url(r'^$', views.cadastro, name='cadastro'),
	url(r'^princiapl/', views.login, name='login'),
	
]