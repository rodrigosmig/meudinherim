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
	valor = forms.DecimalField(
        label = 'Valor',
        min_value = 0.01,
        max_value = 9999.99,
        required = True,
        widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'placeholder': 'Insira o valor'}
        )
    )
	class Meta:
		model = LancamentosCaixa
		fields = ['data', 'categoria', 'descricao', 'valor']