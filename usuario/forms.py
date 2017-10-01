from django import forms 
from django.contrib.auth import get_user_model

class UsuarioForm(forms.Form):

	login = forms.CharField(label = 'Login', max_length=50)
	email = forms.EmailField()
	senha = forms.CharField(label = 'Senha', max_length=50, widget=forms.PasswordInput())
	

class LoginForm(forms.Form):

	login = forms.CharField(label = 'Login', max_length=50)
	senha = forms.CharField(label = 'Senha', max_length=50, widget=forms.PasswordInput())