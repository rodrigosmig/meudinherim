from django.shortcuts import render
from django.http import HttpResponseRedirect
from caixa.models import LancamentosCaixa, Categoria
from caixa.forms import CategoriaForm

def lancamentos(request):
	template = 'caixa/caixa.html'
	lancamentos = LancamentosCaixa.objects.all()
	contexto = {'lancamentos': lancamentos}

	return render(request, template, contexto)

def categoria(request):
	template = 'caixa/categoria.html'
	catEntrada = Categoria.objects.filter(tipo = 1)
	catSaida = Categoria.objects.filter(tipo = 2)
	
	if(request.method == 'POST'):
		form = CategoriaForm(request.POST)
		if(form.is_valid()):
			form.save()
			return HttpResponseRedirect('/caixa/categoria')

	else:
		form = CategoriaForm()

	contexto = {'catEntrada': catEntrada, 'catSaida': catSaida, 'form': form}

	return render(request, template, contexto)
