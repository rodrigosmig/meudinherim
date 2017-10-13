from django.shortcuts import render
from caixa.models import LancamentosCaixa

def lancamentos(request):
	template = 'caixa/caixa.html'
	lancamentos = LancamentosCaixa.objects.all()
	contexto = {'lancamentos': lancamentos}

	return render(request, template, contexto)

# Create your views here.
