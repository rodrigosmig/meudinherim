from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseForbidden
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
from django.contrib import messages
from django.urls import reverse



@login_required
def contasAPagar(request):
	user = request.user
	form = ContasAPagarForm()

	if(request.method == 'POST'):
		form = ContasAPagarForm(request.POST)
		
		try:
			parcelas = int(request.POST.get('parcelas'))
		except ValueError as error:
			messages.warning(request, 'A quantidade de parcelas é inválida.')
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))

		if(parcelas < 1 or parcelas > form.PARCELAS):
			messages.warning(request, 'A quantidade de parcelas é inválida.')
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))

		if(form.is_valid()):
			contaPagar = form.save(commit = False)
			contaPagar.user = request.user
			contaPagar.paga = False
			parcela1 = ""
			
			if(parcelas > 1):
				parcela1 = " 1/" + str(parcelas)

				for x in range(1, parcelas):
					novaParcela = ContasAPagar()
					novaParcela.data = contaPagar.data + datedelta.datedelta(months = x)
					novaParcela.categoria = contaPagar.categoria
					novaParcela.descricao = contaPagar.descricao + " " + str(x + 1) + "/" + str(parcelas)
					novaParcela.valor = contaPagar.valor
					novaParcela.paga = False
					novaParcela.user = request.user
					novaParcela.save()
					
			contaPagar.descricao += parcela1 
			contaPagar.save()
			messages.success(request, "Conta " + contaPagar.descricao + " adicionada com sucesso!")
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))
		else:
			messages.warning(request, "Formulário inválido")

	hoje 		= datetime.today()
	template 	= 'contas_a_pagar/contas_a_pagar.html'	
	contas 		= ContasAPagar.objects.filter(user = user).filter(data__month = hoje.month).filter(data__year = hoje.year)
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
	user = request.user

	if(request.method == 'POST'):		
		idConta = request.POST.get('id_contas_a_pagar')

		try:
			conta = ContasAPagar.objects.get(pk = idConta)
		except ContasAPagar.DoesNotExist as erro:
			messages.warning(request, "Conta não encontrada.")
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))
		except ValueError as erro:
			messages.warning(request, "Conta não encontrada.")
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))

		if(conta.user != user):
			messages.warning(request, "Alteração não permitida.")
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))

		form = ContasAPagarForm(request.POST, instance = conta)
		
		if(form.is_valid()):
			form.save()
			messages.success(request, "Conta " + conta.descricao + " alterada com sucesso!")
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))
		else:
			messages.warning(request, "Formulário inválido")

	
	try:
		idConta = request.GET.get('id_contas_a_pagar', 0)
		conta 	= ContasAPagar.objects.get(pk = idConta)
	except ContasAPagar.DoesNotExist as erro:
		return HttpResponseNotFound("Conta não encontrada.")
	except ValueError as erro:
		return HttpResponseNotFound("Conta não encontrada.")

	if(conta.user != user):
		return HttpResponseForbidden("Alteração não permitida.")

	form = ContasAPagarForm(instance = conta)
	form.getEditCPForm(request)	

	#retorna o id da conta junto com o formulario
	divId = "<div id='id_contaAPagar'>" + idConta + "</div>"

	form_html = {form.as_p(), divId}
	return HttpResponse(form_html)


@login_required
def delContasPagar(request):
	if(request.method == 'POST'):
		user = request.user

		try:
			idConta = request.POST.get('id_contas_a_pagar', 0)
			conta 	= ContasAPagar.objects.get(pk = idConta)
		except ContasAPagar.DoesNotExist as erro:
			messages.warning(request, "Conta não encontrada.")
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))
		except ValueError as erro:
			messages.warning(request, "Conta não encontrada.")
			return HttpResponseRedirect(reverse('contas_a_pagar:index'))
	
		if(conta.user != user):
			return HttpResponseForbidden("Alteração não permitida.")
		
		conta.delete()
		messages.success(request, "Conta " + conta.descricao + " excluída com sucesso!")
		return HttpResponseRedirect(reverse('contas_a_pagar:index'))
	
	messages.warning(request, "Solicitação inválida.")	
	return HttpResponseRedirect(reverse('contas_a_pagar:index'))

#funcao que retorna as agencias do usuario solicitado no pagamento de contas
@login_required
def banco(request):
	if(request.method == 'POST'):
		user = request.user
		bancos = ContaBanco.objects.filter(user = user)
		
		bancosJson = serializers.serialize('json', bancos, use_natural_foreign_keys=True, use_natural_primary_keys=True)

		return HttpResponse(bancosJson, content_type="application/json")

	return HttpResponseServerError("Erro ao requisitar as agências do usuário.")

@login_required
def pagamento(request):
	if(request.method == 'POST'):
		user 			= request.user
		dt_pagamento 	= request.POST.get('data_pagamento', datetime.today())
		tipoPagamento 	= request.POST.get('id_banco', "")

		try:
			idConta = request.POST.get('id_contas_a_pagar', 0)
			conta 	= ContasAPagar.objects.get(pk = idConta)
		except ContasAPagar.DoesNotExist as erro:
			return HttpResponseNotFound("Conta não encontrada.")
		except ValueError as erro:
			return HttpResponseNotFound("Conta não encontrada.")

		if(conta.user != user):
			return HttpResponseForbidden("Alteração não permitida.")

		conta 					= ContasAPagar.objects.get(pk = idConta)
		conta.data_pagamento 	= dt_pagamento
		
		if(tipoPagamento == ""):
			saldoCaixa 					= SaldoCaixa.objects.get(user = user)
			saldoCaixa.saldoAnterior 	= saldoCaixa.saldoAtual
			
			conta.tipo_conta = "c"

			caixa 				= LancamentosCaixa()
			caixa.data 			= conta.data_pagamento
			caixa.categoria 	= conta.categoria
			caixa.descricao 	= conta.descricao
			caixa.valor 		= conta.valor
			caixa.user 			= user
			caixa.conta_a_pagar = conta

			saldoCaixa.saldoAtual -= caixa.valor

			caixa.save()
			saldoCaixa.save()

		else:
			saldoBanco 					= SaldoBanco.objects.get(user = user)
			saldoBanco.saldoAnterior 	= saldoBanco.saldoAtual

			conta.tipo_conta = "b"

			try:
				agencia = ContaBanco.objects.get(pk = tipoPagamento)
			except ContaBanco.DoesNotExist as erro:
				return HttpResponseNotFound("Conta não encontrada.")
			except ValueError as erro:
				return HttpResponseNotFound("Conta não encontrada.")

			if(agencia.user != user):
				return HttpResponseForbidden("Pagamento não permitido.")

			lancamento 		 			= LancamentosBanco()
			lancamento.banco 			= agencia
			lancamento.data 			= conta.data_pagamento
			lancamento.tipo 			= '2'
			lancamento.categoria 		= conta.categoria
			lancamento.descricao 		= conta.descricao
			lancamento. valor 			= conta.valor
			lancamento.user 			= user
			lancamento.conta_a_pagar 	= conta
			
			#altera o saldo da conta
			agencia.saldo -= conta.valor

			agencia.save()
			lancamento.save()

		conta.paga = True
		conta.save()
		
		return HttpResponse("Pagamento efetuado com sucesso")
	return HttpResponseForbidden("Não foi possível efeturar o pagamento.")

@login_required
def cancelaPagamento(request):
	if(request.method == 'POST'):
		user 		= request.user
		idPagamento = request.POST.get('id_contas_a_pagar', 0)

		try:
			conta = ContasAPagar.objects.get(pk = idPagamento)
		except ContasAPagar.DoesNotExist as erro:
			return HttpResponseNotFound("Conta não encontrada.")
		except ValueError as erro:
			return HttpResponseNotFound("Conta não encontrada.")

		if(conta.user != user):
			return HttpResponseForbidden("Alteração não permitida.")

		if(conta.tipo_conta == "c"):
			lancamentoCaixa = LancamentosCaixa.objects.get(conta_a_pagar = conta)
			lancamentoCaixa.delete()
			conta.paga = False
			conta.tipo_conta = None
			conta.data_pagamento = None

			saldoCaixa = SaldoCaixa.objects.get(user = user)
			saldoCaixa.saldoAnterior = saldoCaixa.saldoAtual
			saldoCaixa.saldoAtual += conta.valor
			saldoCaixa.save()
			conta.save()		
		else:
			#busca o lançamento gerado pelo pagamento
			lancamentoBanco = LancamentosBanco.objects.get(conta_a_pagar = conta)

			try:
				agencia = ContaBanco.objects.get(pk = lancamentoBanco.banco.id)
			except ContaBanco.DoesNotExist as erro:
				return HttpResponseNotFound("Conta não encontrada.")
			except ValueError as erro:
				return HttpResponseNotFound("Conta não encontrada.")

			if(agencia.user != user):
				return HttpResponseForbidden("Pagamento não permitido.")
						
			conta.paga 			= False
			conta.tipo_conta 	= None
			agencia.saldo 		+= conta.valor
			
			agencia.save()
			lancamentoBanco.delete()
			conta.save()

		return HttpResponse('Pagamento cancelado com sucesso.')

	return HttpResponseServerError("Não foi possível efeturar o pagamento.")

@login_required
def verificarPagamento(request):
	if(request.method == 'POST'):
		try:
			idPagamento = request.POST.get('id_contas_a_pagar', 0)
			conta 		= ContasAPagar.objects.get(pk = idPagamento)
		except ContasAPagar.DoesNotExist as erro:
			return HttpResponseNotFound("Conta não encontrada.")
		except ValueError as erro:
			return HttpResponseNotFound("Conta não encontrada.")

		if(conta.user != request.user):
			return HttpResponseForbidden("Alteração não permitida.")

		if(conta.paga):
			return HttpResponseForbidden('Conta está paga. Cancele o pagamento antes de excluir.')
		else:
			return HttpResponse(idPagamento)
	else:
		HttpResponseNotFound("Conta não encontrada.")

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