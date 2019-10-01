from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from banco.models import ContaBanco, LancamentosBanco, SaldoBanco
from caixa.models import Categoria, SaldoCaixa
from banco.forms import ContaBancoForm, LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from metas.forms import MetasForm
from metas.models import Metas
from usuario.models import UsuarioProfile
from django.core import serializers
import json
from django.shortcuts import get_object_or_404
from django.urls import reverse
from metas import util

@login_required
def metas(request):
	if(request.method == 'POST'):
		form = MetasForm(request.POST)
		if(form.is_valid()):
			cadastroMeta=form.save(commit = False)
			cadastroMeta.user=request.user
			cadastroMeta.progresso = 0
			cadastroMeta.concluida = False
			cadastroMeta.save()
			messages.success(request, 'Meta ' + cadastroMeta.titulo +  ' cadastrada com sucesso.')
			return HttpResponseRedirect(reverse('metas:metas'))
		else:
			messages.success(request, 'Formulário inválido. Tente novamente.')
			return HttpResponseRedirect(reverse('metas:metas'))

	user = request.user
	template='meta/metas.html'
	contexto = {}

	metas = Metas.objects.filter(user = user)
	contexto['formMetas'] = metas

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = request.user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user).exclude(tipo = ContaBanco.CARTAO_DE_CREDITO)
	contexto['agencias'] = agencias
	
	somaMetas 	= 0
	totalMetas 	= 0

	if agencias:	
		#soma o valor de saldo de todas as agencias
		totalSaldoAgencias = 0
		for a in agencias:
			totalSaldoAgencias += a.saldo

		saldoTotal = totalSaldoAgencias + saldoC.saldoAtual

		for m in metas:
			progresso 	= util.getMetaPercent(m.valor, saldoTotal)
			m.progresso = progresso
			m.save()

			saldoTotal 	-= m.valor
			somaMetas	+= m.valor

	contexto['totalMetas'] = totalMetas
	contexto['somaMetas'] = somaMetas
	
	form = MetasForm() 	

	contexto['formCad'] = form

	userProfile = UsuarioProfile.objects.get(user = request.user)
	contexto['profile'] = userProfile

	#para adicionar lancamento
	formCaixa = LancamentosForm()
	formCaixa.getAddLancamentoForm(request)
	contexto['formLancCaixa'] = formCaixa

	formBanco = LancamentosBancoForm()
	formBanco.getAddLancamentoForm(request, 'banco')
	contexto['formLancBanco'] = formBanco

	formCredito = LancamentosBancoForm()
	formCredito.getAddLancamentoForm(request, 'credito')
	contexto['formLancCredito'] = formCredito
	

	return render(request, template, contexto)

@login_required
def editMeta(request):
	if(request.method == 'POST'):

		#id da meta clicada
		idMeta = request.POST.get('id')
		#busca a meta a ser alterada
		meta = get_object_or_404(Metas, pk = idMeta)

		#atribui a meta ao form	
		form = MetasForm(request.POST, instance = meta)

		if(form.is_valid()):
			form.save()
			messages.success(request, 'Meta ' + meta.titulo +  ' alterada com sucesso.')
			return HttpResponseRedirect(reverse('metas:metas'))
		else:
			messages.error(request, 'Dados inválidos. Tente novamente.')
			return HttpResponseRedirect(reverse('metas:metas'))

	idMeta = request.GET.get('id')

	#busca a meta no banco
	meta = get_object_or_404(Metas, pk = idMeta)

	form = MetasForm(instance = meta)
	form.getEditMetaForm(request)

	#retorna o id da meta junto com o formulario
	divId = "<div id='id_meta'>" + idMeta + "</div>"

	form_html = {form.as_p(), divId}

	return HttpResponse(form_html)

@login_required
def delMeta(request):
	if(request.method == 'POST'):
		#id da meta a ser deletada
		idMeta = request.POST.get('id')

		#busca o lançamento
		meta = get_object_or_404(Metas, pk = idMeta)

		if(request.user == meta.user):
			meta.delete()

			messages.success(request, 'Meta ' + meta.titulo +  ' excluída com sucesso.')
			return HttpResponseRedirect(reverse('metas:metas'))
		else:
			messages.error(request, 'Meta ' + meta.titulo +  ' não pertence ao usuário ' + request.user.username)
			return HttpResponseRedirect(reverse('metas:metas'))

@login_required
def calcMetas(request):
	user = request.user
	saldoC = SaldoCaixa.objects.get(user = user)
	agencias = ContaBanco.objects.filter(user = user).exclude(tipo = ContaBanco.CARTAO_DE_CREDITO)
	metas = Metas.objects.filter(user = user).filter(concluida = False)

	totalSaldoAgencias = 0
	for a in agencias:
		totalSaldoAgencias += a.saldo

	saldoTotal = totalSaldoAgencias + saldoC.saldoAtual

	for m in metas:
		progresso 	= util.getMetaPercent(m.valor, saldoTotal)
		m.progresso = progresso
		m.save()

		saldoTotal 	-= m.valor
	
	metasJson = serializers.serialize('json', metas)
			
	return HttpResponse(metasJson, content_type="application/json")

@login_required
def concluiMeta(request):
	id_meta = request.POST.get('id_meta')
	meta = get_object_or_404(Metas, pk = id_meta)

	if(meta.concluida):
		meta.concluida = False
	else:
		meta.concluida = True
	
	meta.save()

	response = {
		'id': meta.id,
		'msg': "Meta alterada com sucesso",
		'concluida': meta.concluida
	}

	return HttpResponse(json.dumps(response))