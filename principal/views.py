from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from caixa.forms import LancamentosForm
from caixa.models import LancamentosCaixa
from django.contrib.auth.forms import UserCreationForm
from usuario.forms import UsuarioForm
from usuario.forms import LoginForm
import json

def login(request):

	template = 'principal/index.html'

	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():

			form_email = form.cleaned_data['email']
			form_senha = form.cleaned_data['senha']

			usuario = authenticate(username=form_email,password=form_senha)

			if usuario is not None:
				
				return HttpResponseRedirect('/home/')
											#redirecionar para as informações dos usuarios
											# +str(usuario.userprofile.id)
			else:
				return HttpResponseRedirect('/principal/')
													
	else:
		form = LoginForm()

	context = {'form' : form}

	return render(request,template, context)


# FUNCIONANDO NORMAL
#def index(request):
#	return render(request, 'principal/index.html')

def index(request):
	template = 'principal/index.html'

	if request.method == 'POST':
		form = UsuarioForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/principal/')
	else:
		form = UsuarioForm()
		
	context = {'form': UsuarioForm()}

	return render(request, template, context)

def home(request):
	template = 'principal/home.html'
	context = {}

	#carrega os lançamentos do banco de dados
	lancamentos = LancamentosCaixa.objects.all()
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
		titulo = lancamento.descricao + " : " + str(lancamento.valor) 
		eventos.append((titulo, data))

	#converte a tupla para o formato json
	eventos = [{'title': title, 'start': start} for title, start in eventos]
	eventos = json.dumps(eventos, ensure_ascii=False)

	context['events'] = eventos
	

	if(request.method == 'POST'):
		form = LancamentosForm(request.POST)
		if(form.is_valid()):
			form.save()
			return HttpResponseRedirect('/principal/home/')
	else:
		form = LancamentosForm()

		
	context['form'] = form
	return render(request, template, context)