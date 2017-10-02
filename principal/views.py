from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from caixa.forms import LancamentosForm
from caixa.models import LancamentosCaixa
import json

def index(request):
	return render(request, 'principal/index.html')

def home(request):
	template = 'principal/home.html'
	context = {}
	#carrega os lançamentos do banco de dados
	lancamentos = LancamentosCaixa.objects.all()
	eventos = []

	if(request.method == 'POST'):
		form = LancamentosForm(request.POST)
		form.save()
	else:
		form = LancamentosForm()
		

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

	#converte para o formato json
	eventos = [{'title': title, 'start': start} for title, start in eventos]
	eventos = json.dumps(eventos, ensure_ascii=False)
	
	context['events'] = eventos
	context['form'] = form
	return render(request, template, context)

