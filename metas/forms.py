from django.forms import ModelForm
from django import forms
from metas.models import Metas

class MetasForm(ModelForm):
    
    dataInicio = forms.DateField(
        label = 'Data Inicio',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerMI', 'placeholder': 'Insira a início da meta'}
        )
    )

    dataFim = forms.DateField(
        label = 'Data Fim',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerMF', 'placeholder': 'Insira a fim da meta'}
            )
        )

    titulo = forms.CharField(
        label = 'Título da Meta',
        max_length = 40,
        required = True,
        widget = forms.TextInput(
        attrs = {'class': 'form-control', 'placeholder': 'Insira o título da meta'}
        )
    )

    valor = forms.DecimalField(
        label = 'Valor da Meta',
        min_value = 1,
        max_value = 999999.99,
        required = True,
        widget = forms.NumberInput(
        attrs = {'class': 'form-control', 'id': 'id_valor_meta', 'placeholder': 'Insira o valor da meta'}
        )
    )

    class Meta:
        model = Metas
        fields =['dataInicio', 'dataFim', 'titulo', 'valor']