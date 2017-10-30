from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from caixa.forms import LancamentosForm
from caixa.models import LancamentosCaixa, Categoria
from banco.forms import LancamentosBancoForm
from banco.models import LancamentosBanco
from django.contrib.auth.forms import UserCreationForm
from usuario.forms import UsuarioForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django import forms
from banco.models import ContaBanco, LancamentosBanco
import json


def index(request):
	template = 'principal/index.html'

	if request.method == 'POST':
		form = UsuarioForm(request.POST)
		if form.is_valid():
			user = form.save()
			user = authenticate(username = user.username, password = form.cleaned_data['password1'])
			login(request, user)
			return redirect('principal:home')
		else:
			form = LoginForm(request.POST)

			if form.is_valid():

				form_login = form.cleaned_data['login']
				form_senha = form.cleaned_data['senha']

				usuario = authenticate(username=form_login,password=form_senha)

				if usuario is not None:
					login(request, usuario)
					return redirect('principal:home')
	form = UsuarioForm()
	form2 = LoginForm()
	context = {'form': form, 'form2':form2}
	return render(request, template, context)

@login_required
def home(request):
	template = 'principal/home.html'
	context = {}
	#id do usuario logado
	id_user = request.user.id

	#carrega os lançamentos do usuário no banco de dados
	lancamentos = LancamentosCaixa.objects.filter(user_id = id_user)

	eventos = []

	#separa os dados que serão utilizados no calendario em um tupla
	for lancamento in lancamentos:
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
		eventos.append((titulo, data))

	#converte a tupla para o formato json
	eventos = [{'title': title, 'start': start} for title, start in eventos]
	eventos = json.dumps(eventos, ensure_ascii=False)
	context['events'] = eventos

	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control'}
	        )
		)
	
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
	formBanco.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control'}
	        )
		)

	context['formLancCaixa'] = formCaixa
	context['formLancBanco'] = formBanco
	
	return render(request, template, context)