from django.conf.urls import url
from django.conf.urls import include
from principal import views
from django.contrib.auth.views import login, logout

urlpatterns = [    
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', login, {'template_name': 'principal/login.html'}, name='login'),
    url(r'^sair/$', logout, {'next_page': 'principal:index'}, name='logout'),

]