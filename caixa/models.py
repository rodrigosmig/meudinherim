from django.db import models
from django.contrib.auth.models import User
from contas_a_pagar.models import ContasAPagar
from contas_a_receber.models import ContasAReceber
from django.db.models import Count, Sum

# Create your models here.
class LancamentosCaixa(models.Model):

	data = models.DateField()
	categoria = models.ForeignKey('Categoria', on_delete = models.PROTECT)
	descricao = models.CharField(max_length = 100)
	valor = models.DecimalField(max_digits = 6, decimal_places = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	conta_a_pagar = models.ForeignKey(ContasAPagar, on_delete = models.CASCADE, blank = True, null = True)
	conta_a_receber = models.ForeignKey(ContasAReceber, on_delete = models.CASCADE, blank = True, null = True)

	def getLancamentosGroupByCategoria(user, data, tipo_categoria):
		if(tipo_categoria == 'entrada'):
			categoria = 1
		else:
			categoria = 2

		lancamentos = LancamentosCaixa.objects.values(
		'categoria__pk', 'categoria__descricao'
		).annotate(
			valor = Sum('valor'), 
			quantidade = Count('pk')
		).filter(
			user = user
		).filter(
			data__month = data.month
		).filter(
			data__year = data.year
		).filter(
			categoria__tipo = categoria
		)
		
		return lancamentos

	def __str__(self):
		return self.descricao
	
	
	def getLancamentoByCategoria(user, data, categoria):
    		
		lancamentos = LancamentosCaixa.objects.filter(
			user = user
			).filter(
				categoria = categoria
			).filter(
				data__month = data.month
			).filter(
				data__year = data.year
			)

		return lancamentos


class Categoria(models.Model):

	descricao = models.CharField(max_length = 64)
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


