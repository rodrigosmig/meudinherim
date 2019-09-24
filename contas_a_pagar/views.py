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
from datetime import datetime
import datedelta
from usuario.models import UsuarioProfile
from django.core import serializers
import json
from caixa.views import separarCategorias



@login_required
def contasAPagar(request):
	user = request.user

	if(request.method == 'POST'):
		form = ContasAPagarForm(request.POST)
		parcelas = int(request.POST.get('parcelas'))

		if(form.is_valid()):
			contaPagar = form.save(commit = False)
			contaPagar.user = request.user
			contaPagar.paga = False
			contaPagar.save()
			
			if(parcelas > 0):
				parcelas += 1
				for x in range(1, parcelas):
					novaParcela = ContasAPagar()
					novaParcela.data = contaPagar.data + datedelta.datedelta(months = x)
					novaParcela.categoria = contaPagar.categoria
					novaParcela.descricao = contaPagar.descricao + " " + str(x + 1) + "/" + str(parcelas)
					novaParcela.valor = contaPagar.valor
					novaParcela.paga = False
					novaParcela.user = request.user
					novaParcela.save()

			return HttpResponse('Conta a pagar adicionada com sucesso')
		else:
			return HttpResponseServerError("Formulário inválido.")


	template = 'contas_a_pagar/contas_a_pagar.html'

	hoje = datetime.today()

	contas = ContasAPagar.objects.filter(user = user).filter(data__month = hoje.month).filter(data__year = hoje.year)

	form = ContasAPagarForm()
	form.getAddCPForm(request)
	
	context = {'contPagar': contas, 'contPagarForm': form}

	#busca o saldo na carteira do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = user)
	context['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
	context['agencias'] = agencias

	
	#para adicionar lancamento
	formCaixa = LancamentosForm()
	formCaixa.getAddLancamentoForm(request)
	context['formLancCaixa'] = formCaixa

	formBanco = LancamentosBancoForm()
	formBanco.getAddLancamentoForm(request, 'banco')
	context['formLancBanco'] = formBanco

	formCredito = LancamentosBancoForm()
	formCredito.getAddLancamentoForm(request, 'credito')
	context['formLancCredito'] = formCredito

	userProfile = UsuarioProfile.objects.get(user = user)
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
		parcelas = int(request.POST.get('parcelas'))
		
		if(form.is_valid()):
			form.save()

			if(parcelas > 0):
				parcelas += 1
				for x in range(1, parcelas):
					novaParcela = ContasAPagar()
					novaParcela.data = form.cleaned_data['data'] + datedelta.datedelta(months = x)
					novaParcela.categoria = form.cleaned_data['categoria']
					novaParcela.descricao = form.cleaned_data['descricao'] + " " + str(x + 1) + "/" + str(parcelas)
					novaParcela.valor = form.cleaned_data['valor']
					novaParcela.paga = False
					novaParcela.user = request.user
					novaParcela.save()

			return HttpResponse("Conta alterada com sucesso")
		else:
			return HttpResponseServerError("Formulário inválido.")

	#id do lancamento clicado
	idConta = request.GET.get('id')
	conta = ContasAPagar.objects.get(pk = idConta)
	form = ContasAPagarForm(instance = conta)
	form.getEditCPForm(request)	

	#retorna o id da conta junto com o formulario
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
		user = request.user

		dt_pagamento = request.POST.get('data_pagamento')
		tipoPagamento = request.POST.get('banco')

		#busca o saldo do carteira do usuario logado
		saldoCaixa = SaldoCaixa.objects.get(user = user)
		#atribui o valor do saldo anterior
		saldoCaixa.saldoAnterior = saldoCaixa.saldoAtual

		#busca o saldo de Banco do usuario logado
		saldoBanco = SaldoBanco.objects.get(user = user)
		#atribui o valor do saldo anterior
		saldoBanco.saldoAnterior = saldoBanco.saldoAtual
		
		idConta = request.POST.get('id')

		#busca a conta a pagar
		conta = ContasAPagar.objects.get(pk = idConta)
		conta.data_pagamento = dt_pagamento
		conta.save()
		
		#verifica se o pagamento é na carteira ou no banco
		if(tipoPagamento == ""):
			#para pagamento feito na carteira
			conta.tipo_conta = "c"

			#cadastra o lancamento na carteira de acordo com os dados da conta
			caixa = LancamentosCaixa()

			caixa.data = conta.data_pagamento
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

			agencias = ContaBanco.objects.filter(user = user)

			for agencia in agencias:
				if(agencia.banco == tipoPagamento):
					banco = LancamentosBanco()

					banco.banco = agencia
					banco.data = conta.data_pagamento
					banco.tipo = '2'
					banco.categoria = conta.categoria
					banco.descricao = conta.descricao
					banco. valor = conta.valor
					banco.user = request.user
					banco.conta_a_pagar = conta
					
					#altera o saldo da conta
					agencia.saldo -= banco.valor

					agencia.save()
					banco.save()

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
				#deixa a data de pagamento em branco
				conta.data_pagamento = None

				#busca o saldo na carteira do usuario logado e faz o ajuste
				saldoCaixa = SaldoCaixa.objects.get(user = user)
				saldoCaixa.saldoAnterior = saldoCaixa.saldoAtual
				saldoCaixa.saldoAtual += conta.valor
				saldoCaixa.save()
				conta.save()
			
			else:
				#busca o lançamento gerado pelo pagamento
				lancamentoBanco = LancamentosBanco.objects.get(conta_a_pagar = conta)
				
				agencias = ContaBanco.objects.filter(user = user)

				for a in agencias:
					if(a == lancamentoBanco.banco):				
						#muda o status do pagamento
						conta.paga = False
						#deixa em branco o tipo da conta de pagamento
						conta.tipo_conta = None
						#devolve o valor do pagamento
						a.saldo += conta.valor
						a.save()

				#deleta o lançamento gerado pelo pagamento
				lancamentoBanco.delete()
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

@login_required
def filtrarContas(request):
	if(request.method == 'POST'):
		user = request.user
		mes = request.POST.get('mes')
		ano = request.POST.get('ano')
		status = request.POST.get('status')

		if(status == 'todas'):
			contas = ContasAPagar.objects.filter(user = user).filter(data__month = mes).filter(data__year = ano)
		elif(status == 'pagas'):
			contas = ContasAPagar.objects.filter(user = user).filter(data__month = mes).filter(data__year = ano).filter(paga = True)
		elif(status == 'abertas'):
			contas = ContasAPagar.objects.filter(user = user).filter(data__month = mes).filter(data__year = ano).filter(paga = False)

		if(len(contas) != 0):
			contasJson = serializers.serialize('json', contas, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			return HttpResponse(contasJson, content_type="application/json")

		else:
			return HttpResponseServerError("Nenhum conta foi encontrada.")