from django.db import models
from django.contrib.auth.models import User
from contas_a_pagar.models import ContasAPagar
from contas_a_receber.models import ContasAReceber

# Create your models here.
class LancamentosCaixa(models.Model):

	data = models.DateField()
	categoria = models.ForeignKey('Categoria', on_delete = models.CASCADE)
	descricao = models.CharField(max_length = 32)
	valor = models.DecimalField(max_digits = 6, decimal_places = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	conta_a_pagar = models.ForeignKey(ContasAPagar, on_delete = models.CASCADE, blank = True, null = True)
	conta_a_receber = models.ForeignKey(ContasAReceber, on_delete = models.CASCADE, blank = True, null = True)


	def __str__(self):
		return self.descricao


class Categoria(models.Model):

	descricao = models.CharField(max_length = 32)
	TIPOS = (
		("1", "Entrada"),
		("2", "Saida"),
	)
	tipo = models.CharField(choices = TIPOS, max_length = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	#utilizado para enviar o id e descricao quando serializado
	def natural_key(self):
		return (self.id, self.tipo, self.descricao)
		
	def __str__(self):

		return self.descricao

class SaldoCaixa(models.Model):
	saldoAnterior = models.DecimalField(max_digits = 8, decimal_places = 2)
	saldoAtual = models.DecimalField(max_digits = 8, decimal_places = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.saldoAtual)


