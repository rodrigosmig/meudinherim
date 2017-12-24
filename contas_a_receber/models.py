from django.db import models
from django.contrib.auth.models import User

class ContasAReceber(models.Model):

	data = models.DateField()
	categoria = models.ForeignKey('caixa.Categoria', on_delete = models.CASCADE, blank = True)
	descricao = models.CharField(max_length = 64)
	valor = models.DecimalField(max_digits = 8, decimal_places = 2)
	recebido = models.BooleanField(blank = True)
	tipo_conta = models.CharField(max_length = 1, blank = True, null = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)


	def __str__(self):

		return self.descricao
