from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from contas_a_pagar.forms import ContasAPagarForm
from contas_a_pagar.models import ContasAPagar
from contas_a_receber.models import ContasAReceber
from caixa.models import SaldoCaixa, Categoria
from banco.models import ContaBanco
from banco.forms import LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms
from datetime import datetime
from django.core import serializers
import json
from usuario.models import UsuarioProfile
from caixa.views import separarCategorias

@login_required
def relatorioAPagar(request):
	user = request.user

	if(request.method == 'POST'):
		inicio = request.POST['inicio']
		fim = request.POST['fim']
		status = request.POST['status']

		#converte as datas em objetos datetime para fazer o filtro
		data_inicio = datetime.strptime(inicio, "%d/%m/%Y")
		data_fim = datetime.strptime(fim, "%d/%m/%Y")

		if(status == 'abertas'):
			contas = ContasAPagar.objects.filter(data__gte = data_inicio, data__lte = data_fim).filter(user = user).filter(paga = False)
		elif(status == 'pagas'):
			contas = ContasAPagar.objects.filter(data__gte = data_inicio, data__lte = data_fim).filter(user = user).filter(paga = True)
		elif(status == 'vencidas'):
			contas = ContasAPagar.objects.filter(data__gte = data_inicio, data__lt = datetime.now()).filter(user = user).filter(paga = False)

		
		contasJson = serializers.serialize('json', contas, use_natural_foreign_keys=True, use_natural_primary_keys=True)

		return HttpResponse(contasJson, content_type="application/json")
		
	
	template = 'relatorio/relatorio_contas_a_pagar.html'
	contexto = {}

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
	contexto['agencias'] = agencias

	#para adicionar lancamento
	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'].choices = separarCategorias(request)

	formBanco = LancamentosBancoForm()
	#Seleciona apenas o banco do usuario para o formulario
	formBanco.fields['banco'] = forms.ModelChoiceField(
		queryset = ContaBanco.objects.filter(user_id = request.user.id),
		empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
	)
	#seleciona apenas as categorias do usuario logado
	formBanco.fields['categoria'].choices = separarCategorias(request)

	#para adicionar lancamento
	contexto['formLancCaixa'] = formCaixa
	contexto['formLancBanco'] = formBanco

	userProfile = UsuarioProfile.objects.get(user = request.user)
	contexto['profile'] = userProfile

	return render(request, template, contexto)

@login_required
def relatorioAReceber(request):
	user = request.user

	if(request.method == 'POST'):
		inicio = request.POST['inicio']
		fim = request.POST['fim']
		status = request.POST['status']

		#converte as datas em objetos datetime para fazer o filtro
		data_inicio = datetime.strptime(inicio, "%d/%m/%Y")
		data_fim = datetime.strptime(fim, "%d/%m/%Y")

		if(status == 'abertas'):
			contas = ContasAReceber.objects.filter(data__gte = data_inicio, data__lte = data_fim).filter(user = user).filter(recebido = False)
		elif(status == 'recebidas'):
			contas = ContasAReceber.objects.filter(data__gte = data_inicio, data__lte = data_fim).filter(user = user).filter(recebido = True)
		elif(status == 'vencidas'):
			contas = ContasAReceber.objects.filter(data__gte = data_inicio, data__lt = datetime.now()).filter(user = user).filter(recebido = False)

		contasJson = serializers.serialize('json', contas, use_natural_foreign_keys=True, use_natural_primary_keys=True)

		return HttpResponse(contasJson, content_type="application/json")
		
	
	template = 'relatorio/relatorio_contas_a_receber.html'
	contexto = {}

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
	contexto['agencias'] = agencias

	#para adicionar lancamento
	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'].choices = separarCategorias(request)

	formBanco = LancamentosBancoForm()
	#Seleciona apenas o banco do usuario para o formulario
	formBanco.fields['banco'] = forms.ModelChoiceField(
		queryset = ContaBanco.objects.filter(user_id = request.user.id),
		empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
	)
	#seleciona apenas as categorias do usuario logado
	formBanco.fields['categoria'].choices = separarCategorias(request)
	
	#para adicionar lancamento
	contexto['formLancCaixa'] = formCaixa
	contexto['formLancBanco'] = formBanco

	userProfile = UsuarioProfile.objects.get(user = request.user)
	contexto['profile'] = userProfile

	return render(request, template, contexto)