from django.db import models
from django.contrib.auth.models import User
from contas_a_pagar.models import ContasAPagar
from contas_a_receber.models import ContasAReceber
from django.db.models import Count, Sum
from decimal import Decimal

# Create your models here.
class LancamentosCaixa(models.Model):

	data = models.DateField()
	categoria = models.ForeignKey('Categoria', on_delete = models.PROTECT)
	descricao = models.CharField(max_length = 100)
	valor = models.DecimalField(max_digits = 6, decimal_places = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	conta_a_pagar = models.ForeignKey(ContasAPagar, on_delete = models.CASCADE, blank = True, null = True)
	conta_a_receber = models.ForeignKey(ContasAReceber, on_delete = models.CASCADE, blank = True, null = True)

	def __str__(self):
		return self.descricao

	def getLancamentosGroupByCategoria(user, data, tipo_categoria):
		if(tipo_categoria == 'entrada'):
			categoria = Categoria.ENTRADA
		else:
			categoria = Categoria.SAIDA

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
	
	@staticmethod
	def adicionaLancamento(user, descricao, categoria, data, valor):
		valor = Decimal(valor)
		
		lancamento = LancamentosCaixa()
		lancamento.data = data
		lancamento.categoria = categoria
		lancamento.descricao = descricao
		lancamento.valor = valor
		lancamento.user = user
		lancamento.save()

		return lancamento

class Categoria(models.Model):
	ENTRADA = "1"
	SAIDA	= "2"

	TIPOS = (
		("1", "Entrada"),
		("2", "Saida"),
	)

	descricao = models.CharField(max_length = 64)	
	tipo = models.CharField(choices = TIPOS, max_length = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	#utilizado para enviar o id e descricao quando serializado
	def natural_key(self):
		return (self.id, self.tipo, self.descricao)
		
	def __str__(self):

		return self.descricao

	@staticmethod
	def getCategorias(user, tipo):
		return Categoria.objects.filter(user = user).filter(tipo = tipo).order_by("descricao")

	@staticmethod
	def separarCategorias(request):
		user = request.user
		categorias = []
		entrada = []
		saida = []
		for categoria in Categoria.objects.filter(tipo = Categoria.ENTRADA).filter(user = user).order_by('descricao'):
			entrada.append([categoria.id, categoria.descricao])

		for categoria in Categoria.objects.filter(tipo = Categoria.SAIDA).filter(user = user).order_by('descricao'):
			saida.append([categoria.id, categoria.descricao])

		categorias.append(['Entradas', entrada])
		categorias.append(['Saídas', saida])

		return categorias
	
class SaldoCaixa(models.Model):
	saldoAnterior = models.DecimalField(max_digits = 8, decimal_places = 2)
	saldoAtual = models.DecimalField(max_digits = 8, decimal_places = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.saldoAtual)

	@staticmethod
	def getSaldo(user):
		return SaldoCaixa.objects.get(user = user)
	
	def ajusteSaldo(self, categoria, valor):
		self.saldoAnterior = self.saldoAtual
		
		if(categoria.tipo == Categoria.ENTRADA):
			self.saldoAtual += valor
		else:
			self.saldoAtual -= valor
