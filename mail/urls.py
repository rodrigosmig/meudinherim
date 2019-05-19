from django.conf.urls import url
from django.conf.urls import include
from mail import views

urlpatterns = [    
    url(r'^CronContasAPagar/', views.CronContasAPagar, name='CronContasAPagar')
]