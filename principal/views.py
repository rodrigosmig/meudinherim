from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from caixa.forms import LancamentosForm
from caixa.models import LancamentosCaixa
from django.contrib.auth.forms import UserCreationForm
from usuario.forms import UsuarioForm
from usuario.forms import LoginForm
from django.contrib.auth.decorators import login_required
import json


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
	

	if(request.method == 'POST'):
		form = LancamentosForm(request.POST)
		if(form.is_valid()):
			lancamento = form.save(commit = False)
			#relacionao o usuario logado com o lançamento
			lancamento.user = request.user
			lancamento.save()
			return HttpResponseRedirect('/principal/home/')
	else:
		form = LancamentosForm()

		
	context['form'] = form
	return render(request, template, context)