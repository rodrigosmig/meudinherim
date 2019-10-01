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

    prazo = forms.DateField(
		label = 'Prazo',
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control datepicker', 'placeholder': 'Insira o prazo da meta'}
		)
    )

    class Meta:
        model = Metas
        fields =['titulo', 'valor', 'prazo']

    def getEditMetaForm(self, request):
        self.fields['prazo'] = forms.DateField(
            label = 'Prazo',
            required = True,
            widget = forms.TextInput(
                attrs = {'class': 'form-control datepicker', 'id': 'id_prazo-alter_meta', 'placeholder': 'Insira o prazo da meta'}
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