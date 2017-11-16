from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from banco.models import ContaBanco, LancamentosBanco, SaldoBanco
from caixa.models import Categoria, SaldoCaixa
from banco.forms import ContaBancoForm, LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms
from metas.forms import CadastrarMetasForm
from metas.models import Metas
import json

@login_required
def metas(request):
	id_user = request.user.id
	template='meta/metas.html'

	contexto = {}

	metas = Metas.objects.filter(user_id = id_user)
	contexto['formMetas'] = metas

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = request.user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#busca o saldo de Banco do usuario e atribui ao contexto
	saldoB = SaldoBanco.objects.get(user = request.user)
	contexto['saldoBanco'] = saldoB.saldoAtual



	return render(request, template, contexto)


@login_required
def cadastroMeta(request):

	pass



