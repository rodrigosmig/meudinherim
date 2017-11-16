from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Metas(models.Model):
	
	dataInicio = models.DateField()
	dataFim= models.DateField()
	titulo= models.CharField(max_length= 40)
	progresso= models.IntegerField(default=0)
	valor = models.DecimalField(max_digits = 6, decimal_places = 2)
	finalizado= models.BooleanField(blank= True, default= False)
	user = models.ForeignKey(User, on_delete = models.CASCADE, default=1)

	



	
	

	
		