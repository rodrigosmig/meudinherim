from django.forms import ModelForm
from django import forms
from metas.models import Metas

class CadastrarMetasForm(ModelForm):
    
    dataInicio = forms.DateField(
        label = 'Data Inicio',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerMI', 'placeholder': 'Inicio da meta'}
        )
    )

    dataFim = forms.DateField(
        label = 'Data Fim',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerMF', 'placeholder': 'Fim da meta'}
            )
        )

    titulo = forms.CharField(
        label = 'Título da Meta',
        max_length = 40,
        required = True,
        widget = forms.TextInput(
        attrs = {'class': 'form-control', 'placeholder': 'Título da meta'}
        )
    )

    valor = forms.DecimalField(
        label = 'Valor da Meta',
        min_value = 1,
        max_value = 999999.99,
        required = True,
        widget = forms.NumberInput(
        attrs = {'class': 'form-control', 'placeholder': 'Insira o valor da meta'}
        )
    )

    class Meta:
        model= Metas
        fields=['dataInicio', 'dataFim', 'titulo', 'valor']