from django.forms import ModelForm
from django import forms
from banco.models import ContaBanco, LancamentosBanco
from caixa.models import Categoria

class ContaBancoForm(ModelForm):
	banco = forms.CharField(
		label = 'Banco',
		max_length = 32,
		required = True,
		widget = forms.NumberInput(
			attrs = {'class': 'form-control', 'placeholder': 'Nome do Banco'}
		)
    )
	agencia = forms.CharField(
		label = 'Agência',
		max_length = 12,
		required = False,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'placeholder': 'Número da agência'}
		)
    )
	conta = forms.CharField(
    	label = 'Conta',
		max_length = 32,
        required = False,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Número da conta'}
        )
    )
	tipo = forms.ChoiceField(
		widget = forms.Select(
			attrs = {'class': 'form-control'}
		),
		choices = ContaBanco.TIPOS
	)

	class Meta:
		model = ContaBanco
		fields = ['banco', 'agencia', 'conta', 'tipo']