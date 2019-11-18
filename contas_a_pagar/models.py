from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class ContasAPagar(models.Model):

	data = models.DateField()
	data_pagamento = models.DateField(blank = True, null = True)
	categoria = models.ForeignKey('caixa.Categoria', on_delete = models.PROTECT, blank = False, null = False)
	descricao = models.CharField(max_length = 64)
	valor = models.DecimalField(max_digits = 8, decimal_places = 2)
	paga = models.BooleanField(blank = True)
	tipo_conta = models.CharField(max_length = 1, blank = True, null = True)
	user = models.ForeignKey(User, on_delete = models.PROTECT)


	def __str__(self):
		return self.descricao

	@staticmethod
	def getCurrentMmonthAccounts(user):
		hoje = datetime.today()
		contas = ContasAPagar.objects.filter(user = user).filter(data__month = hoje.month).filter(data__year = hoje.year)

		return contas

	@staticmethod
	def getAccountsByStatusAndRangeOfDate(user, status, mes, ano):
		contas = ContasAPagar.objects.filter(user = user).filter(data__month = mes).filter(data__year = ano)
		
		if(status == 'pagas'):
			contas = contas.filter(paga = True)
		elif(status == 'abertas'):
			contas = contas.filter(paga = False)

		return contas
