from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from caixa.forms import LancamentosForm

def index(request):
	return render(request, 'principal/index.html', context)

def home(request):
	if(request.method == 'POST'):
		form = LancamentosForm(request.POST)
		form.save()
		print('teste')
	else:
		form = LancamentosForm()

	context_dict = {'form': form}
	return render(request, 'principal/home.html', context_dict)

