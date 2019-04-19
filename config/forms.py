from django.forms import ModelForm
from django import forms
from caixa.models import ConfigModal

class ConfigForm(ModelForm):
    nick = forms.Charfield(
        label = 'Usuário',
        max_length = 20,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'Digite seu nick'}
        )
    )    
    senha = forms.CharField(
        label = 'Senha',
        max_length = 30,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Digite sua senha'}
        )
    )
    email = forms.Charfield(
    	label = 'Email',
    	required = True,
    	widget = forms.TextInput(
    			attrs = {'class': 'form-control', 'placeholder': 'Digite seu email'}
    		)
    	)

    class Meta:
        model = ConfigModal
        fields = ['nick', 'senha', 'email']