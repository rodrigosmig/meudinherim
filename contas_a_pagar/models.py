from django.db import models
from django.contrib.auth.models import User

class ContasAPagar(models.Model):

	data = models.DateField()
	categoria = models.ForeignKey('caixa.Categoria', on_delete = models.CASCADE, blank = True)
	descricao = models.CharField(max_length = 32)
	valor = models.DecimalField(max_digits = 6, decimal_places = 2)
	paga = models.BooleanField(blank = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)


	def __str__(self):

		return self.descricao
