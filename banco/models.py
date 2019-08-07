from django.db import models
from django.contrib.auth.models import User
from contas_a_pagar.models import ContasAPagar
from contas_a_receber.models import ContasAReceber
from django.core import serializers
from django.db.models import Count, Sum
from datetime import datetime
import json

class ContaBanco(models.Model):
	CONTA_CORRENTE 		= "1"
	CONTA_POUPANCA 		= "2"
	CARTAO_DE_CREDITO 	= "3"

	TIPOS = (
		(CONTA_CORRENTE, "Conta Corrente"),
		(CONTA_POUPANCA, "Conta Poupança"),
		(CARTAO_DE_CREDITO, "Cartão de Crédito"),
	)
	
	banco = models.CharField(max_length = 64)
	agencia = models.CharField(max_length = 10, blank = True, null = True)
	conta = models.CharField(max_length = 20, blank = True, null = True)
	tipo = models.CharField(choices = TIPOS, max_length = 2)
	dia_fechamento = models.CharField(max_length = 2, blank = True, null = True)
	limite = models.DecimalField(max_digits = 7, decimal_places = 2, blank = True, null = True)
	saldo = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0.0)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def natural_key(self):
		return (self.id, self.banco)

	def __str__(self):
		return str(self.banco)

	
	def getLancamentosGroupByCategoria(user, data, tipo_categoria, tipo_conta):
		if(tipo_categoria == 'entrada'):
			categoria = 1
		else:
			categoria = 2

		lancamentos = LancamentosBanco.objects.values(
		'categoria__pk', 'categoria__descricao', 'banco__tipo'
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
		
		if(tipo_conta == 'credito'):
			lancamentos = lancamentos.filter(banco__tipo = ContaBanco.CARTAO_DE_CREDITO)
		else:
			lancamentos = lancamentos.exclude(banco__tipo = ContaBanco.CARTAO_DE_CREDITO)

		return lancamentos
	
	def getLancamentoByCategoria(user, data, categoria, credito = False):
		
		lancamentos = LancamentosBanco.objects.filter(
			user = user
			).filter(
				categoria = categoria
			).filter(
				data__month = data.month
			).filter(
				data__year = data.year
			)
			
		if(credito):
			lancamentos = lancamentos.filter(banco__tipo = ContaBanco.CARTAO_DE_CREDITO)
		else:
			lancamentos = lancamentos.exclude(banco__tipo = ContaBanco.CARTAO_DE_CREDITO)

		return lancamentos

class LancamentosBanco(models.Model):
	banco = models.ForeignKey('ContaBanco', on_delete = models.PROTECT)
	data = models.DateField()
	categoria = models.ForeignKey('caixa.Categoria', on_delete = models.PROTECT)
	TIPOS = (
		("1", "Crédito"),
		("2", "Débito"),
	)
	tipo = models.CharField(choices = TIPOS, max_length = 2)
	descricao = models.CharField(max_length = 128)
	valor = models.DecimalField(max_digits = 7, decimal_places = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	conta_a_pagar = models.ForeignKey(ContasAPagar, on_delete = models.CASCADE, blank = True, null = True)
	conta_a_receber = models.ForeignKey(ContasAReceber, on_delete = models.CASCADE, blank = True, null = True)

	def __str__(self):

		return self.descricao


class SaldoBanco(models.Model):
	saldoAnterior = models.DecimalField(max_digits = 8, decimal_places = 2)
	saldoAtual = models.DecimalField(max_digits = 8, decimal_places = 2)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.saldoAtual)

