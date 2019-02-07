from django.forms import ModelForm
from django import forms
from contas_a_receber.models import ContasAReceber
from caixa.models import Categoria

parcelas = (
    ("0", "Não"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
)

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
        attrs = {'class': 'form-control', 'id': 'id_descricaoCR', 'placeholder': 'Descreva a transação'}
        )
    )
    valor = forms.DecimalField(
        label = 'Valor',
        min_value = 0.01,
        max_value = 999999.99,
        required = True,
        widget = forms.NumberInput(
        attrs = {'class': 'form-control', 'id': 'id_valorCR', 'placeholder': 'Insira o valor'}
        )
    )

    parcelas = forms.ChoiceField(
        label = 'Outras Parcelas',
        widget = forms.Select(
        attrs = {'class': 'form-control', "id": "outras_parcelas"}
        ),
        choices = parcelas
    )

    class Meta:
        model = ContasAReceber
        fields = ['data', 'categoria', 'descricao', 'valor']