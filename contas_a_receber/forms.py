from django.forms import ModelForm
from django import forms
from contas_a_receber.models import ContasAReceber
from caixa.models import Categoria

class ContasAReceberForm(ModelForm):
	data = forms.DateField(
        label = 'Data',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerCR', 'placeholder': 'Vencimento'}
        )
    )
	descricao = forms.CharField(
		label = 'Descrição',
        max_length = 64,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Descreva a transação'}
        )
    )
	valor = forms.DecimalField(
		label = 'Valor',
        min_value = 0.01,
        max_value = 999999.99,
        required = True,
        widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'placeholder': 'Insira o valor'}
        )
    )

	class Meta:
		model = ContasAReceber
		fields = ['data', 'categoria', 'descricao', 'valor']