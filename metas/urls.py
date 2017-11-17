from django.conf.urls import url
from django.conf.urls import include
from metas import views

urlpatterns = [   

    url(r'^$', views.metas, name='metas'),
    url(r'^edit/', views.editMeta, name='edit'),
    url(r'^delete/', views.delMeta, name='delete'), 
]