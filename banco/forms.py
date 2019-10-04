from django.forms import ModelForm
from django import forms
from banco.models import ContaBanco, LancamentosBanco
from caixa.models import Categoria

class ContaBancoForm(ModelForm):
	banco = forms.CharField(
		label = 'Banco',
		max_length = 64,
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'id_banco_agencia', 'placeholder': 'Nome do Banco'}
		)
    )
	agencia = forms.CharField(
		label = 'Agência',
		max_length = 10,
		required = False,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'placeholder': 'Número da agência'}
		)
    )
	conta = forms.CharField(
    	label = 'Conta',
		max_length = 20,
        required = False,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Número da conta'}
        )
    )
	tipo = forms.ChoiceField(
		widget = forms.Select(
			attrs = {'class': 'form-control', 'id': 'id_tipo_agencia'}
		),
		choices = ContaBanco.TIPOS
	)
	dia_fechamento = forms.IntegerField(
    	label = 'Dia do fechamento',
		min_value = 1,
        max_value = 31,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Exemplo: 31'}
        )
    )
	limite = forms.DecimalField(
        label = 'Limite',
        min_value = 0.00,
        max_value = 99999.99,
        required = True,
        widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'placeholder': '99999.99'}
        )
    )

	class Meta:
		model = ContaBanco
		fields = ['banco', 'agencia', 'conta', 'tipo', 'dia_fechamento', 'limite']

	def getEditBancoForm(self):
		self.fields['banco'].widget.attrs['id'] = "id_banco-alter_banco"
		self.fields['agencia'].widget.attrs['id'] = "id_agencia-alter_agencia"
		self.fields['conta'].widget.attrs['id'] = "id_conta-alter_conta"
		self.fields['tipo'].widget.attrs['id'] = "id_tipo-alter_tipo"
		self.fields['dia_fechamento'].widget.attrs['id'] = "id_conta-alter_dia_fechamento"
		self.fields['limite'].widget.attrs['id'] = "id_tipo-alter_limite"


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
		max_length = 128,
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
		model 		= LancamentosBanco
		fields 		= ['data', 'banco', 'tipo', 'categoria', 'descricao', 'valor']

	def getAddLancamentoForm(self, request, tipo):
		id_banco = "id_banco"

		if(tipo == 'banco'):
			query = ContaBanco.objects.filter(user = request.user).exclude(tipo = ContaBanco.CARTAO_DE_CREDITO)
			label = "Banco"
		else:
			query 		= ContaBanco.objects.filter(user = request.user).filter(tipo = ContaBanco.CARTAO_DE_CREDITO)
			label 		= "Cartão de Crédito"
			id_banco	= "id_banco_credito"

			self.fields['data'].widget.attrs['id'] 		= "datePicker_credito"
			self.fields['banco'].widget.attrs['id'] 	= "id_banco_credito"
			self.fields['tipo'].widget.attrs['id'] 		= "id_tipo_credito"
			self.fields['categoria'].widget.attrs['id'] = "categoria_credito"
			self.fields['descricao'].widget.attrs['id'] = "desc_credito"
			self.fields['valor'].widget.attrs['id'] 	= "valor_credito"			
		
		self.fields['banco'] = forms.ModelChoiceField(
			label = label,
			queryset = query,
			empty_label = 'Nenhum',
			widget = forms.Select(
				attrs = {'class': 'form-control', 'id': id_banco}
			)
		)
		self.fields['categoria'].choices = Categoria.separarCategorias(request)

	def getEditLancamentoForm(self, request):
		self.fields['banco'] = forms.ModelChoiceField(
				queryset = ContaBanco.objects.filter(user = request.user),
				empty_label = 'Nenhum',
				widget = forms.Select(
					attrs = {'class': 'form-control', 'id': 'id_banco-alter_banco'}
				)
			)
		#seleciona apenas as categorias do usuario logado
		self.fields['categoria'].choices = Categoria.separarCategorias(request)
		
		self.fields['data'] = forms.DateField(
			label = 'Data',
			required = True,
			widget = forms.TextInput(
				attrs = {'class': 'form-control', 'id': 'datepicker-alter_banco'}
			)
		)
		self.fields['tipo'] = forms.ChoiceField(
			widget = forms.Select(
				attrs = {'class': 'form-control', 'id': 'id_tipo-alter_banco'}
			),
			choices = LancamentosBanco.TIPOS
		)
		self.fields['valor'] = forms.DecimalField(
			label = 'Valor',
			min_value = 0.01,
			max_value = 9999.99,
			required = True,
			widget = forms.NumberInput(
				attrs = {'class': 'form-control', 'id': 'id_valor-alter_banco'}
			)
		)
		self.fields['descricao'] = forms.CharField(
			label = 'Descrição',
			max_length = 32,
			required = True,
			widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'id_descricao-alter_banco'}
			)
		)