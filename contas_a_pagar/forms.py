from django.forms import ModelForm
from django import forms
from contas_a_pagar.models import ContasAPagar
from caixa.models import Categoria

parcelas = (
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
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
)

class ContasAPagarForm(ModelForm):
    PARCELAS = 15
    
    data = forms.DateField(
        label = 'Data de vencimento',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepickerCP', 'placeholder': 'Vencimento'}
        )
    )
    descricao = forms.CharField(
        label = 'Descrição',
        max_length = 64,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'id_descricaoCP', 'placeholder': 'Descreva a transação'}
        )
    )
    valor = forms.DecimalField(
        label = 'Valor',
        min_value = 0.01,
        max_value = 999999.99,
        required = True,
        widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'id': 'id_valorCP', 'placeholder': 'Insira o valor'}
        )
    )
    categoria = forms.ModelChoiceField(
        queryset = Categoria.objects.all(),
        empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
    )
    parcelas = forms.ChoiceField(
        label = 'Parcelas',
        required    = False,
        widget = forms.Select(
            attrs = {'class': 'form-control', "id": "outras_parcelas"}
        ),
        choices = parcelas
    )
    class Meta:
        model = ContasAPagar
        fields = ['data', 'categoria', 'descricao', 'valor']
    
    def getAddCPForm(self, request):
        #seleciona apenas as categorias do usuario logado e do tipo saida
        self.fields['categoria'] = forms.ModelChoiceField(
                queryset = Categoria.objects.filter(user = request.user).filter(tipo = 2).order_by('descricao'),
                empty_label = 'Nenhum',
                widget = forms.Select(
                    attrs = {'class': 'form-control', 'id': 'id_categoriaCP'}
                )
            )
    
    def getEditCPForm(self, request):
        #seleciona apenas as categorias do usuario logado e do tipo saida
        self.fields['categoria'] = forms.ModelChoiceField(
                queryset = Categoria.objects.filter(user = request.user).filter(tipo = 2),
                empty_label = 'Nenhum',
                widget = forms.Select(
                    attrs = {'class': 'form-control', 'id': 'id_categoria_edit'}
                )
            )
        self.fields['data'] = forms.DateField(
            label = 'Data de vencimento',
            required = True,
            widget = forms.TextInput(
                attrs = {'class': 'form-control', 'id': 'datepickerCP_edit'}

            )
        )
        self.fields['descricao'] = forms.CharField(
            label = 'Descrição',
            max_length = 32,
            required = True,
            widget = forms.TextInput(
                attrs = {'class': 'form-control', 'id': 'id_descricao_edit'}
            )
        )
        self.fields['valor'] = forms.DecimalField(
            label = 'Valor',
            min_value = 0.01,
            max_value = 999999.99,
            required = True,
            widget = forms.NumberInput(
                attrs = {'class': 'form-control', 'id': 'id_valor_edit'}
            )
        )

        del self.fields["parcelas"]