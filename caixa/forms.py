from django.forms import ModelForm
from django import forms
from caixa.models import LancamentosCaixa, Categoria


class LancamentosForm(ModelForm):
    data = forms.DateField(
        label = 'Data',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerC'}
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
    categoria = forms.ModelChoiceField(
        queryset = Categoria.objects.all(),
        empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
    )
    class Meta:
        model = LancamentosCaixa
        fields = ['data', 'categoria', 'descricao', 'valor']


class CategoriaForm(ModelForm):
    tipo = forms.ChoiceField(
        widget = forms.Select(
            attrs = {'class': 'form-control', 'id': 'id_tipo_categoria'}
        ),
        choices = Categoria.TIPOS
    )
    descricao = forms.CharField(
        label = 'Descrição',
        max_length = 32,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'id_descricao_categoria', 'placeholder': 'Descreva a categoria'}
        )
    )
    class Meta:
        model = Categoria
        fields = ['tipo', 'descricao']