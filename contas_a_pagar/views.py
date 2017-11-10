from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from contas_a_pagar.forms import ContasAPagarForm
from contas_a_pagar.models import ContasAPagar
from caixa.models import Categoria, SaldoCaixa, LancamentosCaixa
from banco.models import SaldoBanco, ContaBanco
from django import forms
from django.core import serializers
import json

@login_required
def contasAPagar(request):
	if(request.method == 'POST'):
		form = ContasAPagarForm(request.POST)
		print(form)
		if(form.is_valid()):
			contaPagar = form.save(commit = False)
			contaPagar.user = request.user
			contaPagar.paga = False
			contaPagar.save()
			return HttpResponseRedirect('/contas_a_pagar/')

	template = 'contas_a_pagar/contas_a_pagar.html'

	contas = ContasAPagar.objects.filter(user = request.user)

	form = ContasAPagarForm()
	#seleciona apenas as categorias do usuario logado e do tipo saida
	form.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id).filter(tipo = 2),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control'}
	        )
		)

	context = {'contPagar': contas, 'contPagarForm': form}

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = request.user)
	context['saldoCaixa'] = saldoC.saldoAtual

	#busca o saldo de Banco do usuario e atribui ao contexto
	saldoB = SaldoBanco.objects.get(user = request.user)
	context['saldoBanco'] = saldoB.saldoAtual

	return render(request, template, context)

@login_required
def editContasPagar(request):
	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id
		#id do lancamento clicado
		idConta = request.POST.get('id')
		print(idConta)
		#busca o lancamento a ser alterado
		conta = ContasAPagar.objects.get(pk = idConta)

		print(conta)
		
		print(request.POST)
		
		#atribui o lancamento ao form	
		form = ContasAPagarForm(request.POST, instance = conta)

		
		if(form.is_valid()):
			form.save()

			return HttpResponse("Conta alterada com sucesso")
		else:
			return HttpResponseServerError("Formulário inválido")

	#id do lancamento clicado
	idConta = request.GET.get('id')
	conta = ContasAPagar.objects.get(pk = idConta)
	form = ContasAPagarForm(instance = conta)

	#seleciona apenas as categorias do usuario logado e do tipo saida
	form.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id).filter(tipo = 2),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control', 'id': 'id_categoria_edit'}
	        )
		)

	#altera o id dos campos
	form.fields['data'] = forms.DateField(
		label = 'Data',
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'datepickerCP_edit'}

        )
	)
	form.fields['descricao'] = forms.CharField(
		label = 'Descrição',
		max_length = 32,
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'id_descricao_edit'}
        )
    )
	form.fields['valor'] = forms.DecimalField(
		label = 'Valor',
		min_value = 0.01,
    	max_value = 999999.99,
    	required = True,
    	widget = forms.NumberInput(
    		attrs = {'class': 'form-control', 'id': 'id_valor_edit'}
        )
    )

	#retorna o id do lancamento junto com o formulario
	divId = "<div id='id_contaAPagar'>" + idConta + "</div>"

	form_html = {form.as_p(), divId}
	return HttpResponse(form_html)


@login_required
def delContasPagar(request):
	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id
		#id do lancamento a ser deletado
		idConta = request.POST.get('id')

		#busca o lançamento
		conta = ContasAPagar.objects.get(pk = idConta)		
		
		if(request.user.id == conta.user_id):
			conta.delete()
			
			return HttpResponse("Conta a pagar excluída com sucesso")
		else:
			return HttpResponseServerError("Conta não encontrado.")
		

	return HttpResponseServerError("Conta não encontrado.")

#funcao que retorna as agencias do usuario solicitado no pagamento de contas
@login_required
def banco(request):
	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id
		bancos = ContaBanco.objects.filter(user_id = id_user)
		
		bancosJson = serializers.serialize('json', bancos, use_natural_foreign_keys=False, use_natural_primary_keys=False)

		return HttpResponse(bancosJson, content_type="application/json")

	return HttpResponseServerError("Banco não encontrado")


def pagamento(request):
	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id

		tipoPagamento = request.POST.get('banco')

		#busca o saldo do usuario logado
		saldo = SaldoCaixa.objects.get(user = request.user)
		#atribui o valor do saldo anterior
		saldo.saldoAnterior = saldo.saldoAtual
		
		idConta = request.POST.get('id')

		#busca a conta a pagar
		conta = ContasAPagar.objects.get(pk = idConta)

		#verifica se o pagamento é no caixa ou no banco
		if(tipoPagamento == ""):
			
			#cadastra o lancamento do caixa de acordo com os dados da conta
			caixa = LancamentosCaixa()

			caixa.data = conta.data
			caixa.categoria = conta.categoria
			caixa.descricao = conta.descricao
			caixa. valor = conta.valor
			caixa.user = request.user

			#atribui o novo saldo de acordo com a categoria do lançamento
			if(caixa.categoria.tipo == "1"):
				saldo.saldoAtual += caixa.valor
			else:
				saldo.saldoAtual -= caixa.valor
			
			caixa.save()
			saldo.save()
	
		else:

			bancos = ContaBanco.objects.filter(user_id = id_user)

			for banco in bancos:
				if(banco.banco == tipoPagamento):
					print(banco.banco)
					print("imprimiu")
		
		
		conta.paga = True
		conta.save()
		
		return HttpResponse("Pagamento efetuado com sucesso")