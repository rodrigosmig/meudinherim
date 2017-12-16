from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from contas_a_pagar.forms import ContasAPagarForm
from contas_a_pagar.models import ContasAPagar
from caixa.models import Categoria, SaldoCaixa, LancamentosCaixa
from banco.models import SaldoBanco, ContaBanco, LancamentosBanco
from banco.forms import LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms
from usuario.models import UsuarioProfile
from django.core import serializers
import json

@login_required
def contasAPagar(request):
	if(request.method == 'POST'):
		form = ContasAPagarForm(request.POST)

		if(form.is_valid()):
			contaPagar = form.save(commit = False)
			contaPagar.user = request.user
			contaPagar.paga = False
			contaPagar.save()
			return HttpResponse('Conta a pagar adicionada com sucesso')

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

	#para adicionar lancamento
	# context['formLancCaixa'] = formCaixa
	# context['formLancBanco'] = formBanco

	userProfile = UsuarioProfile.objects.get(user = request.user)
	context['profile'] = userProfile

	return render(request, template, context)

@login_required
def editContasPagar(request):
	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id
		#id do lancamento clicado
		idConta = request.POST.get('id')

		#busca o lancamento a ser alterado
		conta = ContasAPagar.objects.get(pk = idConta)
		
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

@login_required
def pagamento(request):
	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id

		tipoPagamento = request.POST.get('banco')

		#busca o saldo do caixa do usuario logado
		saldoCaixa = SaldoCaixa.objects.get(user = request.user)
		#atribui o valor do saldo anterior
		saldoCaixa.saldoAnterior = saldoCaixa.saldoAtual

		#busca o saldo de Banco do usuario logado
		saldoBanco = SaldoBanco.objects.get(user = request.user)
		#atribui o valor do saldo anterior
		saldoBanco.saldoAnterior = saldoBanco.saldoAtual
		
		idConta = request.POST.get('id')

		#busca a conta a pagar
		conta = ContasAPagar.objects.get(pk = idConta)

		#verifica se o pagamento é no caixa ou no banco
		if(tipoPagamento == ""):
			#para pagamento feito no caixa
			conta.tipo_conta = "c"

			#cadastra o lancamento do caixa de acordo com os dados da conta
			caixa = LancamentosCaixa()

			caixa.data = conta.data
			caixa.categoria = conta.categoria
			caixa.descricao = conta.descricao
			caixa. valor = conta.valor
			caixa.user = request.user
			caixa.conta_a_pagar = conta

			#diminui o saldo do usuário
			saldoCaixa.saldoAtual -= caixa.valor
			
			caixa.save()
			saldoCaixa.save()
	
		else:
			#para pagamento feito no banco
			conta.tipo_conta = "b"

			agencias = ContaBanco.objects.filter(user_id = id_user)

			for agencia in agencias:
				if(agencia.banco == tipoPagamento):
					banco = LancamentosBanco()

					banco.banco = agencia
					banco.data = conta.data
					banco.tipo = '2'
					banco.categoria = conta.categoria
					banco.descricao = conta.descricao
					banco. valor = conta.valor
					banco.user = request.user
					banco.conta_a_pagar = conta
					
					saldoBanco.saldoAtual -= banco.valor

					banco.save()
					saldoBanco.save()

		conta.paga = True
		conta.save()
		
		return HttpResponse("Pagamento efetuado com sucesso")

@login_required
def cancelaPagamento(request):
	if(request.method == 'POST'):
		user = request.user
		idPagamento = request.POST.get('id')

		conta = ContasAPagar.objects.get(pk = idPagamento)

		if(conta.user == user):
			if(conta.tipo_conta == "c"):
				#busca o lançamento gerado pelo pagamento
				lancamentoCaixa = LancamentosCaixa.objects.get(conta_a_pagar = conta)
				#deleta o lançamento gerado pelo pagamento
				lancamentoCaixa.delete()
				#muda o status do pagamento
				conta.paga = False
				#deixa em branco o tipo da conta de pagamento
				conta.tipo_conta = None

				#busca o saldo do caixa do usuario logado e faz o ajuste
				saldoCaixa = SaldoCaixa.objects.get(user = user)
				saldoCaixa.saldoAnterior = saldoCaixa.saldoAtual
				saldoCaixa.saldoAtual += conta.valor
				saldoCaixa.save()
				conta.save()
			
			else:
				#busca o lançamento gerado pelo pagamento
				lancamentoBanco = LancamentosBanco.objects.get(conta_a_pagar = conta)
				#deleta o lançamento gerado pelo pagamento
				lancamentoBanco.delete()
				#muda o status do pagamento
				conta.paga = False
				#deixa em branco o tipo da conta de pagamento
				conta.tipo_conta = None

				#busca o saldo do caixa do usuario logado e faz o ajuste
				saldoBanco = SaldoBanco.objects.get(user = user)
				saldoBanco.saldoAnterior = saldoBanco.saldoAtual
				saldoBanco.saldoAtual += conta.valor
				saldoBanco.save()
				conta.save()

			return HttpResponse('Pagamento cancelado com sucesso.')


	return HttpResponseServerError("Pagamento não encontrado. Tente novamente.")

@login_required
def verificarPagamento(request):
	if(request.method == 'POST'):
		idPagamento = request.POST.get('id')
		conta = ContasAPagar.objects.get(pk = idPagamento)
		if(conta.paga):
			return HttpResponseServerError('Conta está paga. Cancele o pagamento antes de excluir.')
		else:
			return HttpResponse(idPagamento)
	else:
		HttpResponseServerError("Conta inexistente")