from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from usuario.forms import EditAccountsForm

def config(request):
    id_user = request.user.id
    template = 'config/config.html'
    contexto = {}

    user = User.objects.get(pk = id_user)

    #Editar
    if(request.method == 'POST'):
    	form = EditAccountsForm(request.POST, instance = request.user)
    	if form.is_valid():
    		form.save()
    		form = EditAccountsForm(instance = request.user)
    		contexto['success'] = True
    	else:
    		form = EditAccountsForm(instance = request.user)

    form = EditAccountsForm(instance = request.user)
    contexto = {'formConfig': form }

    return render(request, template, contexto)

    #Editar Senha
    if(request.method == 'POST'):
    	form = PasswordChangeForm(request.POST, instance = request.user)
    	if form.is_valid():
    		form.save()
    		form = PasswordChangeForm(instance = request.user)
    		contexto['success'] = True
    	else:
    		form = PasswordChangeForm(instance = request.user)

    form = PasswordChangeForm(instance = request.user)
    contexto = {'formConfig2': form }

    return render(request, template, contexto)
