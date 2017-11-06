from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from contas_a_pagar.forms import ContasAPagarForm
from contas_a_pagar.models import ContasAPagar
from caixa.models import Categoria
from django import forms

@login_required
def contasAPagar(request):
	if(request.method == 'POST'):
		form = ContasAPagarForm(request.POST)
		print(form)
		if(form.is_valid()):
			contaPagar = form.save(commit = False)
			contaPagar.user = request.user
			contaPagar.paga = False
			contaPagar.save()
			return HttpResponseRedirect('/contas_a_pagar/contasAPagar/')

	template = 'contas_a_pagar/contas_a_pagar.html'

	contas = ContasAPagar.objects.filter(user = request.user)

	form = ContasAPagarForm()
	#seleciona apenas as categorias do usuario logado e do tipo saida
	form.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id).filter(tipo = 2),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control'}
	        )
		)

	context = {'contPagar': contas, 'contPagarForm': form}

	print('sdlkfnas;ldfn;sldnfk;alsdnkf;laskdnf;lasnkdf;lasnkdlf;nasdkn')

	return render(request, template, context)
