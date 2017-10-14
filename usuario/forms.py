from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class UsuarioForm(forms.Form):

# 	login = forms.CharField(label = 'Login', max_length=50)
# 	email = forms.EmailField()
# 	senha = forms.CharField(label = 'Senha', max_length=50, widget=forms.PasswordInput())
	

class LoginForm(forms.Form):

 	email = forms.EmailField(label = 'E-mail')
 	senha = forms.CharField(label = 'Senha', max_length=50, widget=forms.PasswordInput())

# adicionando o campo email no formulario do cadastro
class UsuarioForm(UserCreationForm):

	email = forms.EmailField(label='E-mail')


	# sobreescrevendo o save de UserCreationForm
	def save (self, commit = True):

		user = super(UsuarioForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user 

	# verifica se tem possui o email (tem que fazer a nível de banco ainda)
	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Já existe um usuário com esse e-mail')
		return email