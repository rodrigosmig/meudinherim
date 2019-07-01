from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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
from datetime import datetime
from django.db.models import Count, Sum
import locale

def index(request):
	template = 'principal/index.html'
	form = RegisterForm()

	if request.method == 'POST':

		form = RegisterForm(request.POST)

		if form.is_valid():
			print("Usuário")
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
	template = 'principal/home.html'
	context = {}
	#id do usuario logado
	user = request.user

	userProfile = UsuarioProfile.objects.get(user = user)
	context['profile'] = userProfile

	""" eventosCaixa = []
	eventosBanco = []
	eventosCPagar = []
	eventosCReceber = []

	#carrega os lançamentos do caixa do usuário
	lancamentosCaixa = LancamentosCaixa.objects.filter(user = user)
	#carrega os lançamentos do banco do usuário
	lancamentosBanco = LancamentosBanco.objects.filter(user = user)
	#carrega as contas a pagar do usuário
	contasAPagar = ContasAPagar.objects.filter(user = user).filter(paga = False)
	#carrega as contas a receber do usuário
	contasAReceber = ContasAReceber.objects.filter(user = user).filter(recebido = False)

	#separa os dados do caixa que serão utilizados no calendario em um tupla
	for lancamento in lancamentosCaixa:
		dia = str(lancamento.data.day)
		if(len(dia) == 1):
			dia = "0" + dia
		mes = str(lancamento.data.month)
		if(len(mes) == 1):
			mes = "0" + mes
		ano = str(lancamento.data.year)
		#concatena a data para o formato do fullcalendar
		data = ano + "-" + mes + "-" + dia
		titulo = lancamento.descricao + " : " + " R$" + str(lancamento.valor) 
		eventosCaixa.append((titulo, data))
	
	#converte a tupla para dicionario
	eventosCaixa = [{'title': title, 'start': start} for title, start in eventosCaixa]

	#separa os dados do banco que serão utilizados no calendario em um tupla
	for lancamento in lancamentosBanco:
		dia = str(lancamento.data.day)
		if(len(dia) == 1):
			dia = "0" + dia
		mes = str(lancamento.data.month)
		if(len(mes) == 1):
			mes = "0" + mes
		ano = str(lancamento.data.year)
		#concatena a data para o formato do fullcalendar
		data = ano + "-" + mes + "-" + dia
		titulo = lancamento.descricao + " : " + " R$" + str(lancamento.valor) 
		eventosBanco.append((titulo, data))

	#converte a tupla para para dicionario
	eventosBanco = [{'title': title, 'start': start, 'color': 'yellow', 'textColor': 'black'} for title, start in eventosBanco]

	#separa os dados do contas a pagar que serão utilizados no calendario em um tupla
	for conta in contasAPagar:
		dia = str(conta.data.day)
		if(len(dia) == 1):
			dia = "0" + dia
		mes = str(conta.data.month)
		if(len(mes) == 1):
			mes = "0" + mes
		ano = str(conta.data.year)
		#concatena a data para o formato do fullcalendar
		data = ano + "-" + mes + "-" + dia
		titulo = conta.descricao + " : " + " R$" + str(conta.valor) 
		eventosCPagar.append((titulo, data))

	#converte a tupla para para dicionario
	eventosCPagar = [{'title': title, 'start': start, 'color': 'red'} for title, start in eventosCPagar]

	#separa os dados do contas a receber que serão utilizados no calendario em um tupla
	for conta in contasAReceber:
		dia = str(conta.data.day)
		if(len(dia) == 1):
			dia = "0" + dia
		mes = str(conta.data.month)
		if(len(mes) == 1):
			mes = "0" + mes
		ano = str(conta.data.year)
		#concatena a data para o formato do fullcalendar
		data = ano + "-" + mes + "-" + dia
		titulo = conta.descricao + " : " + " R$" + str(conta.valor) 
		eventosCReceber.append((titulo, data))

	#converte a tupla para para dicionario
	eventosCReceber = [{'title': title, 'start': start, 'color': 'green'} for title, start in eventosCReceber]

	
	#junta os lancamento de caixa, banco e contas a pagar
	todosEventos = eventosBanco + eventosCaixa + eventosCPagar + eventosCReceber
	#converte para o formato Json
	todosEventos = json.dumps(todosEventos, ensure_ascii=False)

	context['events'] = todosEventos """
	
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
	hoje = datetime.today()
	total_entradas 	= 0
	total_saidas 	= 0

	#calcula total de entradas
	banco_entrada = LancamentosBanco.objects.values(
		'categoria__descricao'
		).annotate(
			valor = Sum('valor'), 
			quantidade = Count('pk')
		).filter(
			data__month = hoje.month
		).filter(
			data__year = hoje.year
		).filter(categoria__tipo = 1)
	
	for b in banco_entrada:
		total_entradas += b['valor']

	caixa_entrada = LancamentosCaixa.objects.values(
		'categoria__descricao'
		).annotate(
			valor = Sum('valor'), 
			quantidade = Count('pk')
		).filter(
			data__month = hoje.month
		).filter(
			data__year = hoje.year
		).filter(categoria__tipo = 1)	

	for c in caixa_entrada:
		total_entradas += c['valor']


	#calcula total de saidas
	banco_saida = LancamentosBanco.objects.values(
		'categoria__descricao'
		).annotate(
			valor = Sum('valor'), 
			quantidade = Count('pk')
		).filter(
			data__month = hoje.month
		).filter(
			data__year = hoje.year
		).filter(categoria__tipo = 2)
	
	for b in banco_saida:
		total_saidas += b['valor']

	caixa_saida = LancamentosCaixa.objects.values(
		'categoria__descricao'
		).annotate(
			valor = Sum('valor'), 
			quantidade = Count('pk')
		).filter(
			data__month = hoje.month
		).filter(
			data__year = hoje.year
		).filter(categoria__tipo = 2)	

	for c in caixa_saida:
		total_saidas += c['valor']
	
	context['total_entradas'] = locale.currency(total_entradas, grouping=True, symbol=None)
	context['total_saidas'] = locale.currency(total_saidas, grouping=True, symbol=None)
	
	contas_abertas = ContasAPagar.objects.filter(data__month__lte = hoje.month).filter(data__year__lte = hoje.year).filter(user = user).filter(paga = False)
	contas_vencidas = ContasAPagar.objects.filter(data__lt = hoje).filter(user = user).filter(paga = False)

	context['quant_contas_abertas'] = len(contas_abertas)
	context['quant_contas_vencidas'] = len(contas_vencidas)


	#teste = [{'title': title, 'start': start, 'color': 'red'} for title, start in eventosCPagar]

	#print(banco_entrada.values_list(), "1333")
	#print(banco_entrada)

	categorias = []
	categorias_total = 0
	

	for b in banco_saida:
		categorias.append({'label': b['categoria__descricao'], 'value': b['valor'], 'quantidade': b['quantidade']})
		categorias_total += b['valor']
		
	for c in caixa_saida:
		for l in categorias:			
			if(c['categoria__descricao'] == l['label']):
				l['value'] += c['valor']
				l['quantidade'] += c['quantidade']
				categorias_total += c['valor']
				break	
	
	context['gastos_categoria'] = sorted(categorias, key = lambda i: (i['value'], i['quantidade']), reverse = True)
	print(categorias)
	categorias_json = json.dumps(categorias, ensure_ascii=False, use_decimal = True)
	context['gastos_categoria_json'] = categorias_json
	context['categorias_total'] = categorias_total

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
	saldoC = SaldoCaixa.objects.get(user = user)
	context['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
	context['agencias'] = agencias

	context['formLancCaixa'] = formCaixa
	context['formLancBanco'] = formBanco

	#soma o valor de saldo de todas as agencias
	totalSaldoAgencias = 0
	for a in agencias:
		totalSaldoAgencias += a.saldo

	return render(request, template, context)