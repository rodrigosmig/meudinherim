from django.forms import ModelForm
from django import forms
from caixa.models import LancamentosCaixa


class LancamentosForm(ModelForm):
	data = forms.DateField(
        label = 'Data',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Ex: 06/06/2006'}
        )
    )
	descricao = forms.CharField(
        label = 'Descrição',
        max_length = 32,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Descreva a transação'}
        )
    )
	valor = forms.CharField(
        label = 'Valor',
        max_length = 6,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Insira o valor'}
        )
    )
	class Meta:
		model = LancamentosCaixa
		fields = ['data', 'categoria', 'descricao', 'valor']