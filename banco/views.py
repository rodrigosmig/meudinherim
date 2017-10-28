from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from banco.models import ContaBanco, LancamentosBanco
from banco.forms import ContaBancoForm

@login_required
def cadastroBanco(request):
	id_user = request.user.id

	template = 'banco/agencia.html'
	agencias = ContaBanco.objects.filter(user_id = id_user)
	form_agencia = ContaBancoForm()

	context = {'formAgencia': form_agencia, 'agencias': agencias}

	return render(request, template, context)

@login_required
def banco(request):
	#id do usuario logado
	id_user = request.user.id
	template = 'banco/banco.html'
	lancamentos = LancamentosBanco.objects.filter(user_id = id_user)
	contexto = {'lancBanco': lancamentos}

	return render(request, template, contexto)