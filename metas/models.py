from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Metas(models.Model):
	
	titulo		= models.CharField(max_length = 40)
	progresso	= models.DecimalField(max_digits = 5, decimal_places = 2)
	prazo		= models.DateField(default=date.today)
	valor 		= models.DecimalField(max_digits = 8, decimal_places = 2)
	concluida 	= models.BooleanField(blank = True, default = False)
	user 		= models.ForeignKey(User, on_delete = models.CASCADE, default=1)

	def __str__(self):
		return self.titulo

	class Meta:
		ordering = ['prazo', 'valor']	



	
	

	
		