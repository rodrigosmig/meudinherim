from django.forms import ModelForm
from django import forms
from metas.models import Metas

class MetasForm(ModelForm):

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
        fields =['titulo', 'valor']

    def getEditMetaForm(self, request):
        self.fields['dataInicio'] = forms.DateField(
            label = 'Data Inicio',
            required = True,
            widget = forms.TextInput(
                attrs = {'class': 'form-control', 'id': 'datepickerMI-alter_meta', 'placeholder': 'Insira a início da meta'}
            )
        )

        self.fields['dataFim'] = forms.DateField(
            label = 'Data Fim',
            required = True,
            widget = forms.TextInput(
                attrs = {'class': 'form-control', 'id': 'datepickerMF-alter_meta', 'placeholder': 'Insira a fim da meta'}
                )
            )

        self.fields['titulo'] = forms.CharField(
            label = 'Título da Meta',
            max_length = 40,
            required = True,
            widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'id_titulo-alter_meta', 'placeholder': 'Insira o título da meta'}
            )
        )

        self.fields['valor'] = forms.DecimalField(
            label = 'Valor da Meta',
            min_value = 1,
            max_value = 999999.99,
            required = True,
            widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'id': 'id_valor-alter_meta', 'placeholder': 'Insira o valor da meta'}
            )
        )