from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from contas_a_pagar.forms import ContasAPagarForm
from contas_a_pagar.models import ContasAPagar
from datetime import datetime
from django.core import serializers
import json

@login_required
def relatorioAPagar(request):
	user = request.user

	if(request.method == 'POST'):
		inicio = request.POST['inicio']
		fim = request.POST['fim']
		status = request.POST['status']

		#converte as datas em objetos datetime para fazer o filtro
		data_inicio = datetime.strptime(inicio, "%d/%m/%Y")
		data_fim = datetime.strptime(fim, "%d/%m/%Y")

		if(status == 'a_pagar'):
			contas = ContasAPagar.objects.filter(data__gte = data_inicio, data__lte = data_fim).filter(user = user).filter(paga = False)
		elif(status == 'pagas'):
			contas = ContasAPagar.objects.filter(data__gte = data_inicio, data__lte = data_fim).filter(user = user).filter(paga = True)
		elif(status == 'vencidas'):
			contas = ContasAPagar.objects.filter(data__gte = data_inicio, data__lte = datetime.now()).filter(user = user).filter(paga = False)

		
		contasJson = serializers.serialize('json', contas, use_natural_foreign_keys=True, use_natural_primary_keys=True)

		return HttpResponse(contasJson, content_type="application/json")
		
	
	template = 'relatorio/relatorio_contas_a_pagar.html'

	return render(request, template)

@login_required
def relatorioAReceber(request):
	template = 'relatorio/relatorio_contas_a_receber.html'
	return render(request, template)
