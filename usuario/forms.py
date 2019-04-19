from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from usuario.models import UsuarioProfile

# class UsuarioForm(forms.Form):

# 	login = forms.CharField(label = 'Login', max_length=50)
# 	email = forms.EmailField()
# 	senha = forms.CharField(label = 'Senha', max_length=50, widget=forms.PasswordInput())
	

class LoginForm(forms.Form):

 	login = forms.CharField(
 		label = 'login', 
 		max_length=50,
 		required = True,
 		widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'id_username_login', 'placeholder': 'Usuário'}
        )
 	)
 	senha = forms.CharField(
 		label = 'Senha', 
 		max_length=50, 
 		widget=forms.PasswordInput(
 			attrs = {'class': 'form-control', 'id': 'id_password_login', 'placeholder': 'Senha'}
 		))

# adicionando o campo email no formulario do cadastro
class RegisterForm(UserCreationForm):

	email = forms.EmailField(label='E-mail')

	def __init__ (self, *args, **kwargs):
		super (RegisterForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({'class': 'form-control'})

		self.fields['username'].widget.attrs['placeholder'] = 'Nome do usuário'
		self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
		self.fields['password1'].widget.attrs['placeholder'] = 'Digite sua senha'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'

	# sobreescrevendo o save de UserCreationForm
	def save (self, commit = True):

		user = super(RegisterForm, self).save(commit=False)
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


class EditAccountsForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EditAccountsForm, self).__init__(*args, **kwargs)        
		self.fields['username'].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
		self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
		self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'required': 'required'})

	def clean_email(self):
		email = self.cleaned_data['email']
		queryset = User.objects.filter(email = email).exclude(pk = self.instance.pk)
		if(queryset.exists()):
			raise forms.ValidationError('Já existe usuário com este email')
		return email

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name']

class UsuarioProfileForm(ModelForm):
	class Meta:
		model = UsuarioProfile
		fields = ['foto']