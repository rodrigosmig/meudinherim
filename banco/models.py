from django.db import models
from django.contrib.auth.models import User
from contas_a_pagar.models import ContasAPagar
from contas_a_receber.models import ContasAReceber
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json

class ContaBanco(models.Model):
	banco = models.CharField(max_length = 32)
	agencia = models.CharField(max_length = 10, blank = True, null = True)
	conta = models.CharField(max_length = 20, blank = True, null = True)
	TIPOS = (
		("1", "Conta Corrente"),
		("2", "Conta Poupança"),
	)
	tipo = models.CharField(choices = TIPOS, max_length = 2)
	saldo = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0.0)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def natural_key(self):
		return (self.id, self.banco)

	def __str__(self):
		return str(self.banco)


class LancamentosBanco(models.Model):
	banco = models.ForeignKey('ContaBanco', on_delete = models.CASCADE)
	data = models.DateField()
	categoria = models.ForeignKey('caixa.Categoria', on_delete = models.CASCADE)
	TIPOS = (
		("1", "Crédito"),
		("2", "Débito"),
	)
	tipo = models.CharField(choices = TIPOS, max_length = 2)
	descricao = models.CharField(max_length = 32)
	valor = models.DecimalField(max_digits = 6, decimal_places = 2)
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

