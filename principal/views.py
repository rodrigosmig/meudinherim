from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from caixa.forms import LancamentosForm
from caixa.models import LancamentosCaixa, Categoria, SaldoCaixa
from banco.forms import LancamentosBancoForm
from banco.models import LancamentosBanco, ContaBanco, SaldoBanco
from contas_a_pagar.models import ContasAPagar
from contas_a_receber.models import ContasAReceber
from django.contrib.auth.forms import  AuthenticationForm
from usuario.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django import forms
from banco.models import ContaBanco, LancamentosBanco, SaldoBanco
from caixa.models import SaldoCaixa
from metas.models import Metas
from usuario.models import UsuarioProfile
import simplejson as json
from django.contrib import messages
from django.conf import settings
from caixa.views import separarCategorias
from datetime import datetime, date
from django.db.models import Count, Sum
import locale
from django.core import serializers
from dateutil.relativedelta import relativedelta
from json import dumps

def index(request):
	template = 'principal/index.html'
	form = RegisterForm()

	if request.method == 'POST':

		form = RegisterForm(request.POST)

		if form.is_valid():
			user = form.save()

			#criar saldo caixa para o usuario
			saldoC = SaldoCaixa()
			saldoC.saldoAnterior = 0
			saldoC.saldoAtual = 0
			saldoC.user = user
			saldoC.save()

			#criar saldo banco para o usuario
			saldoB = SaldoBanco()
			saldoB.saldoAnterior = 0
			saldoB.saldoAtual = 0
			saldoB.user = user
			saldoB.save()

			#criar registro na tabela de foto
			userFoto = UsuarioProfile()
			userFoto.user = user
			userFoto.save()

			user = authenticate(username = user.username, password = form.cleaned_data['password1'])
			login(request, user)
			return redirect('principal:home')

	#instancia o formulario de login com a classe para o bootstrap
	formLogin = AuthenticationForm()
	formLogin.fields['username'] = forms.CharField(
 		label = 'login', 
 		max_length=50,
 		required = True,
 		widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Usuário'}
        )
 	)
	formLogin.fields['password'] = forms.CharField(
 		label = 'Senha', 
 		max_length=50, 
 		widget=forms.PasswordInput(
 			attrs = {'class': 'form-control', 'placeholder': 'Senha'}
 		))
	
	context = {'form': form, 'formLogin':formLogin}

	return render(request, template, context)


def entrar(request):
	if(request.method == 'POST'):
		user = authenticate(username = request.POST['username'], password = request.POST['password'])
				
		if user is not None:
			login(request, user)
			return redirect(settings.LOGIN_REDIRECT_URL)
		else:
			messages.error(request, 'Login ou senha inválidos. Tente novamente.')
			#return redirect('principal:login')
	
	template = 'principal/login.html'
	formLogin = AuthenticationForm()
	contexto = {'form': formLogin}

	return render(request, template, contexto)

@login_required
def home(request):
	template 	= 'principal/home.html'
	context 	= {}
	user 		= request.user

	userProfile = UsuarioProfile.objects.get(user = user)
	context['profile'] = userProfile
	
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
	
	if 'data' in request.session:
		data = datetime.strptime(request.session.get('data'), "%Y-%m-%d %H-%M-%S")
	else:
		data = datetime.today()
	
	if(request.method == 'POST' and 'mes' in request.POST):
		tipo_mes = request.POST.get('mes')

		if(tipo_mes == 'anterior'):
			data = data - relativedelta(months = 1)
		else:
			data = data + relativedelta(months = 1)
		
		request.session['data'] = data.strftime("%Y-%m-%d %H-%M-%S")

		return redirect('principal:home')

	total_credito 	= 0
	total_entradas 	= 0
	total_saidas 	= 0
	entradas_array	= []
	saidas_array	= []

	#calcula total de entradas
	banco_entrada = ContaBanco.getLancamentosGroupByCategoria(user, data, 'entrada', 'banco')

	for b in banco_entrada:
		entradas_array.append(b)
		total_entradas += b['valor']

	caixa_entrada = LancamentosCaixa.getLancamentosGroupByCategoria(user, data, 'entrada')

	for c in caixa_entrada:
		descricao_categoria = ""
		for b in entradas_array:
			if(c['categoria__descricao'] == b['categoria__descricao']):
				b['quantidade'] 	+= c['quantidade']
				b['valor']			+= c['valor']
				descricao_categoria	= c['categoria__descricao']
				break
		if(c['categoria__descricao'] != descricao_categoria):
			entradas_array.append(c)
		total_entradas += c['valor']

	#calcula total de saidas
	banco_saida = ContaBanco.getLancamentosGroupByCategoria(user, data, 'saida', 'banco')
	
	for b in banco_saida:
		saidas_array.append(b)
		total_saidas += b['valor']

	caixa_saida = LancamentosCaixa.getLancamentosGroupByCategoria(user, data, 'saida')
	
	for c in caixa_saida:
		descricao_categoria = ""
		for b in saidas_array:
			if(c['categoria__descricao'] == b['categoria__descricao']):
				b['quantidade'] 	+= c['quantidade']
				b['valor']			+= c['valor']
				descricao_categoria	= c['categoria__descricao']
				break
		if(c['categoria__descricao'] != descricao_categoria):
			saidas_array.append(c)
		total_saidas += c['valor']
	
	#calcula total de lançamentos do cartão de crédito
	cartao_credito = ContaBanco.getLancamentosGroupByCategoria(user, data, 'saida', 'credito')

	for cr in cartao_credito:
		total_credito += cr['valor']
	
	context['total_entradas'] 		= locale.currency(total_entradas, grouping=True, symbol=None)
	context['total_saidas'] 		= locale.currency(total_saidas, grouping=True, symbol=None)
	context['total_credito'] 		= locale.currency(total_credito, grouping=True, symbol=None)
	
	contas_abertas 					= ContasAPagar.objects.filter(data__month__lte = data.month).filter(data__year__lte = data.year).filter(user = user).filter(paga = False)
	context['contas_abertas'] 		= contas_abertas	
	context['quant_contas_abertas'] = len(contas_abertas)

	categorias_entrada 			= []
	categorias_saida 			= []
	categorias_credito 			= []
	categorias_entradas_total 	= 0
	categorias_saidas_total 	= 0
	categorias_credito_total 	= 0

	for cr in cartao_credito:
		categorias_credito.append({'categoria_id': cr['categoria__pk'], 'label': cr['categoria__descricao'], 'tipo': cr['banco__tipo'], 'value': cr['valor'], 'quantidade': cr['quantidade']})
		categorias_credito_total += cr['valor']

	for e in entradas_array:
		tipo = 'caixa'
		if('banco__tipo' in e):
			tipo = e['banco__tipo']		
		categorias_entrada.append({'categoria_id': e['categoria__pk'], 'tipo': tipo, 'label': e['categoria__descricao'], 'value': e['valor'], 'quantidade': e['quantidade']})
		categorias_entradas_total += e['valor']

	for s in saidas_array:
		tipo = 'caixa'
		if('banco__tipo' in s):
			tipo = s['banco__tipo']		
		categorias_saida.append({'categoria_id': s['categoria__pk'], 'tipo': tipo, 'label': s['categoria__descricao'], 'value': s['valor'], 'quantidade': s['quantidade']})
		categorias_saidas_total += s['valor']

	context['categoria_saida'] 			= sorted(categorias_saida, key = lambda i: (i['value'], i['quantidade']), reverse = True)
	categorias_saidas_json 				= json.dumps(categorias_saida, ensure_ascii=False, use_decimal = True)
	context['categoria_saida_json']		= categorias_saidas_json
	context['categorias_saidas_total'] 	= categorias_saidas_total

	context['categoria_entrada'] 		= sorted(categorias_entrada, key = lambda i: (i['value'], i['quantidade']), reverse = True)
	categorias_entrada_json 			= json.dumps(categorias_entrada, ensure_ascii=False, use_decimal = True)
	context['categoria_entrada_json'] 	= categorias_entrada_json
	context['categorias_entrada_total'] = categorias_entradas_total
	
	context['categoria_credito'] 		= sorted(categorias_credito, key = lambda i: (i['value'], i['quantidade']), reverse = True)
	categorias_credito_json 			= json.dumps(categorias_credito, ensure_ascii=False, use_decimal = True)
	context['categoria_credito_json'] 	= categorias_credito_json
	context['categorias_credito_total']  = categorias_credito_total

	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'].choices = separarCategorias(request)
	
	formBanco = LancamentosBancoForm()
	#Seleciona apenas o banco do usuario para o formulario
	formBanco.fields['banco'] = forms.ModelChoiceField(
		queryset = ContaBanco.objects.filter(user = user),
		empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
	)
	#seleciona apenas as categorias do usuario logado
	formBanco.fields['categoria'].choices = separarCategorias(request)

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC 					= SaldoCaixa.objects.get(user = user)
	context['saldoCaixa'] 	= saldoC.saldoAtual

	#para saldo de cada agencia
	agencias 			= ContaBanco.objects.filter(user = user)
	context['agencias'] = agencias

	context['formLancCaixa'] = formCaixa
	context['formLancBanco'] = formBanco
	context['data'] = data
	#soma o valor de saldo de todas as agencias
	totalSaldoAgencias = 0
	for a in agencias:
		totalSaldoAgencias += a.saldo
	
	return render(request, template, context)

def detalhesLancamento(request):
	user = request.user
	hoje = datetime.today()
	
	id_categoria 	= request.GET.get('categoria_id')
	tipo_conta	 	= request.GET.get('tipo_conta')

	categoria = Categoria.objects.filter(id = id_categoria)

	if not categoria:
		return HttpResponseNotFound()
	
	if 'data' in request.session:
		data = datetime.strptime(request.session.get('data'), "%Y-%m-%d %H-%M-%S")
	else:
		data = datetime.today()
	
	if tipo_conta == ContaBanco.CARTAO_DE_CREDITO:
		
		lancamentos 		= ContaBanco.getLancamentoByCategoria(user, data, categoria, True)
		lancamentos_json	= serializers.serialize('json', lancamentos, use_natural_foreign_keys=True, use_natural_primary_keys=True)
		
		return HttpResponse(lancamentos_json, content_type="application/json")
	
	else:
		lancamentos_array = []
		
		lancamentos_banco	= ContaBanco.getLancamentoByCategoria(user, data, categoria)
		lancamentos_caixa 	= LancamentosCaixa.getLancamentoByCategoria(user, data, categoria)

		for l in lancamentos_banco:
			lancamentos_array.append(l)
		
		for lc in lancamentos_caixa:
			lancamentos_array.append(lc)

		lancamentos_json = serializers.serialize('json', lancamentos_array, use_natural_foreign_keys=True, use_natural_primary_keys=True)
		return HttpResponse(lancamentos_json, content_type="application/json")
		


	return HttpResponse("OK")