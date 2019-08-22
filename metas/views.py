from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from banco.models import ContaBanco, LancamentosBanco, SaldoBanco
from caixa.models import Categoria, SaldoCaixa
from banco.forms import ContaBancoForm, LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from metas.forms import MetasForm
from metas.models import Metas
from usuario.models import UsuarioProfile
from django.core import serializers
import json
from caixa.views import separarCategorias
from django.shortcuts import get_object_or_404

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
			return HttpResponse('Meta cadastrada com sucesso.')
		else:
			return HttpResponseServerError('Formulário inválido. Tente novamente.')

	user = request.user
	template='meta/metas.html'
	contexto = {}

	metas = Metas.objects.filter(user = user)
	contexto['formMetas'] = metas

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = request.user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
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
			if(saldoTotal >= m.valor):
				m.progresso = 100.00
			else:
				progresso = (saldoTotal / m.valor) * 100
				m.progresso = round(progresso, 2)
			somaMetas += m.valor
			m.save()

		if(saldoTotal > somaMetas):
			totalMetas = 100.00
		else:
			progressoTotal = (saldoTotal / somaMetas) * 100
			totalMetas = round(progressoTotal, 2)

	contexto['totalMetas'] = totalMetas
	contexto['somaMetas'] = somaMetas
	
	form = MetasForm() 	

	contexto['formCad'] = form

	userProfile = UsuarioProfile.objects.get(user = request.user)
	contexto['profile'] = userProfile


	#para adicionar lancamento
	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'].choices = separarCategorias(request)

	#para adicionar lancamento
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
	

	return render(request, template, contexto)

@login_required
def editMeta(request):
	user = request.user

	if(request.method == 'POST'):

		#id da meta clicada
		idMeta = request.POST.get('id')
		#busca a meta a ser alterado
		meta = Metas.objects.get(pk = idMeta)
		
		#atribui a meta ao form	
		form = MetasForm(request.POST, instance = meta)

		if(form.is_valid()):
			form.save()

			return HttpResponse('Meta alterada com sucesso')
		else:
			return HttpResponseServerError('Dados inválidos. Tente novamente')

	idMeta = request.GET.get('id')

	#busca a meta no banco
	meta = Metas.objects.get(pk = idMeta)

	form = MetasForm(instance = meta)

	form.fields['dataInicio'] = forms.DateField(
		label = 'Data Inicio',
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'datepickerMI-alter_meta', 'placeholder': 'Insira a início da meta'}
        )
    )

	form.fields['dataFim'] = forms.DateField(
		label = 'Data Fim',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerMF-alter_meta', 'placeholder': 'Insira a fim da meta'}
            )
        )

	form.fields['titulo'] = forms.CharField(
        label = 'Título da Meta',
        max_length = 40,
        required = True,
        widget = forms.TextInput(
        attrs = {'class': 'form-control', 'id': 'id_titulo-alter_meta', 'placeholder': 'Insira o título da meta'}
        )
    )

	form.fields['valor'] = forms.DecimalField(
        label = 'Valor da Meta',
        min_value = 1,
        max_value = 999999.99,
        required = True,
        widget = forms.NumberInput(
        attrs = {'class': 'form-control', 'id': 'id_valor-alter_meta', 'placeholder': 'Insira o valor da meta'}
        )
    )

	#retorna o id da meta junto com o formulario
	divId = "<div id='id_meta'>" + idMeta + "</div>"

	form_html = {form.as_p(), divId}

	return HttpResponse(form_html)

@login_required
def delMeta(request):
	if(request.method == 'POST'):
		#id do usuario
		user = request.user
		#id da meta a ser deletada
		idMeta = request.POST.get('id')

		#busca o lançamento
		meta = Metas.objects.get(pk = idMeta)		
		if(request.user == meta.user):
			meta.delete()

			return HttpResponse("Meta excluída com sucesso")
		else:
			return HttpResponseServerError("Meta não encontrada.")
		

	return HttpResponseServerError("Meta não encontrada.")

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
		if(saldoTotal >= m.valor):
			m.progresso = 100.00
		else:
			progresso = (saldoTotal / m.valor) * 100
			m.progresso = round(progresso, 2)
		m.save()

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