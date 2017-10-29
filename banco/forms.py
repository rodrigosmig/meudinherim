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



class LancamentosBancoForm(ModelForm):
	data = forms.DateField(
		label = 'Data',
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'datepickerB'}
		)
    )
	descricao = forms.CharField(
		label = 'Descrição',
		max_length = 32,
		required = True,
		widget = forms.TextInput(
		attrs = {'class': 'form-control', 'id': 'desc_Banco', 'placeholder': 'Descreva a transação'}
        )
    )
	tipo = forms.ChoiceField(
		widget = forms.Select(
            attrs = {'class': 'form-control'}
        ),
        choices = LancamentosBanco.TIPOS
    )
	valor = forms.DecimalField(
        label = 'Valor',
        min_value = 0.01,
        max_value = 9999.99,
        required = True,
        widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'id': 'valor_banco', 'placeholder': 'Insira o valor'}
        )
    )
	categoria = forms.ModelChoiceField(
        queryset = Categoria.objects.all(),
        empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control', 'id': 'categoria_banco'}
        )
    )

	class Meta:
		model = LancamentosBanco
		fields = ['banco', 'data', 'tipo', 'categoria', 'descricao', 'valor']