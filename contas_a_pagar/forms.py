from django.forms import ModelForm
from django import forms
from contas_a_pagar.models import ContasAPagar
from caixa.models import Categoria

class ContasAPagarForm(ModelForm):
	data = forms.DateField(
        label = 'Data',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerCP', 'placeholder': 'Vencimento'}
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
        max_value = 999999.99,
        required = True,
        widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'placeholder': 'Insira o valor'}
        )
    )
	categoria = forms.ModelChoiceField(
        queryset = Categoria.objects.all(),
        empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
    )

	class Meta:
		model = ContasAPagar
		fields = ['data', 'categoria', 'descricao', 'valor']