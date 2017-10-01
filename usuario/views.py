from django.shortcuts import render
from usuario.forms import UsuarioForm
from usuario.forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from usuario.models import UsuarioProfile
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def cadastro(request):

	if request.method == 'POST':
		form = UsuarioForm(request.POST)

		if form.is_valid():
			login = form.cleaned_data['login']
			email = form.cleaned_data['email']
			senha = form.cleaned_data['senha']

			novo_usuario = User.objects.create_user(username=login,
													password=senha)
			novo_usuario.save()

			novo_perfil = UsuarioProfile(user = novo_usuario, email = email)
			novo_perfil.save()

			return HttpResponseRedirect('/principal/')

	else:
		form = UsuarioForm()

	context_dict = {'form': form}
	return render(request,'templates/principal/index.html',context=context_dict)

def login(request):

	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():

			form_login = form.cleaned_data['login']
			form_senha = form.cleaned_data['senha']

			usuario = authenticate(username=form_login,password=form_senha)

			if usuario is not None:
				
				return HttpResponseRedirect('/home/')
											#redirecionar para as informações dos usuarios
											# +str(usuario.userprofile.id)
			else:
				return HttpResponseRedirect('/principal/')
													
	else:
		form = LoginForm()

	context_dict = {'form' : form}

	return render(request,'templates/principal/index.html',context= context_dict)