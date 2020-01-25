from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from caixa.models import Categoria, SaldoCaixa, LancamentosCaixa
from banco.models import SaldoBanco, ContaBanco, LancamentosBanco
from banco.forms import LancamentosBancoForm
from caixa.forms import LancamentosForm
from contas_a_receber.models import ContasAReceber
from contas_a_receber.forms import ContasAReceberForm
from django import forms
import datedelta
from django.core import serializers
import json
from usuario.models import UsuarioProfile
from caixa.views import separarCategorias
from django.contrib import messages
from django.urls import reverse
import datetime

@login_required
def contasAReceber(request):
	user = request.user
	form = ContasAReceberForm()

	if(request.method == 'POST'):
		form = ContasAReceberForm(request.POST)
		
		try:
			parcelas = int(request.POST.get('parcelas'))
		except ValueError as error:
			messages.warning(request, 'A quantidade de parcelas é inválida.')
			return HttpResponseRedirect(reverse('contas_a_receber:index'))
		
		if(parcelas < 1 or parcelas > form.PARCELAS):
			messages.warning(request, 'A quantidade de parcelas é inválida.')
			return HttpResponseRedirect(reverse('contas_a_receber:index'))


		if(form.is_valid()):
			contReceber 			= form.save(commit = False)
			contReceber.user 		= request.user
			contReceber.recebido 	= False
			parcela1 				= ""
			mensagem 				= contReceber.descricao
			
			if(parcelas > 1):
				parcela1 = " 1/" + str(parcelas)

				for x in range(1, parcelas):
					novaParcela = ContasAReceber()
					novaParcela.data = contReceber.data + datedelta.datedelta(months = x)
					novaParcela.categoria = contReceber.categoria
					novaParcela.descricao = contReceber.descricao + " " + str(x + 1) + "/" + str(parcelas)
					novaParcela.valor = contReceber.valor
					novaParcela.recebido = False
					novaParcela.user = user
					novaParcela.save()
			
			contReceber.descricao += parcela1 
			contReceber.save()
			messages.success(request, "Conta " + mensagem + " adicionada com sucesso!")
			return HttpResponseRedirect(reverse('contas_a_receber:index'))
		else:
			messages.warning(request, "Formulário inválido")


	template 	= 'contas_a_receber/contas_a_receber.html'	
	contas 		= ContasAReceber.getCurrentMmonthAccounts(user)
	form 		= ContasAReceberForm()
	form.getAddCRForm(request)	

	contexto = {'contReceber': contas, 'contReceberForm': form}

	#busca o saldo na carteira do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
	contexto['agencias'] = agencias

	#para adicionar lancamento
	formCaixa = LancamentosForm()
	formCaixa.getAddLancamentoForm(request)
	contexto['formLancCaixa'] = formCaixa

	formBanco = LancamentosBancoForm()
	formBanco.getAddLancamentoForm(request, 'banco')
	contexto['formLancBanco'] = formBanco

	formCredito = LancamentosBancoForm()
	formCredito.getAddLancamentoForm(request, 'credito')
	contexto['formLancCredito'] = formCredito

	userProfile = UsuarioProfile.objects.get(user = request.user)
	contexto['profile'] = userProfile

	return render(request, template, contexto)

@login_required
def editContasReceber(request):
	user = request.user

	if(request.method == 'POST'):
		idConta = request.POST.get('id_contas_a_receber')

		try:
			conta = ContasAReceber.objects.get(pk = idConta)
			print(conta)
		except ContasAReceber.DoesNotExist as erro:
			messages.warning(request, "Conta não encontrada.")
			return HttpResponseRedirect(reverse('contas_a_receber:index'))
		except ValueError as erro:
			messages.warning(request, "Conta não encontrada.")
			return HttpResponseRedirect(reverse('contas_a_receber:index'))

		if(conta.user != user):
			messages.warning(request, "Alteração não permitida.")
			return HttpResponseRedirect(reverse('contas_a_receber:index'))

		form = ContasAReceberForm(request.POST, instance = conta)

		if(form.is_valid()):
			form.save()
			messages.success(request, "Conta " + conta.descricao + " alterada com sucesso!")
			return HttpResponseRedirect(reverse('contas_a_receber:index'))
		else:
			messages.warning(request, "Formulário inválido")
			print(form)
	
	try:
		idConta = request.GET.get('id_contas_a_receber', 0)
		conta 	= ContasAReceber.objects.get(pk = idConta)
	except ContasAReceber.DoesNotExist as erro:
		return HttpResponseNotFound("Conta não encontrada.")
	except ValueError as erro:
		return HttpResponseNotFound("Conta não encontrada.")

	if(conta.user != user):
		return HttpResponseForbidden("Alteração não permitida.")

	form = ContasAReceberForm(instance = conta)
	form.getEditCRForm(user)	

	#retorna o id da conta junto com o formulario
	divId = "<div id='id_contaAReceber'>" + idConta + "</div>"

	form_html = {form.as_p(), divId}

	return HttpResponse(form_html)

@login_required
def verificarRecebimento(request):
	if(request.method == 'POST'):
		try:
			idRecebimento 	= request.POST.get('id_contas_a_receber', 0)
			conta 			= ContasAReceber.objects.get(pk = idRecebimento)
		except ContasAReceber.DoesNotExist as erro:
			return HttpResponseNotFound("Conta não encontrada.")
		except ValueError as erro:
			return HttpResponseNotFound("Conta não encontrada.")

		if(conta.user != request.user):
			return HttpResponseForbidden("Alteração não permitida.")

		if(conta.recebido):
			return HttpResponseForbidden('Conta foi recebida. Cancele o recebimento antes de excluir.')

		return HttpResponse(idRecebimento)

@login_required
def delContasReceber(request):
	if(request.method == 'POST'):
		user = request.user

		try:
			idRecebimento 	= request.POST.get('id_contas_a_receber', 0)
			conta 			= ContasAReceber.objects.get(pk = idRecebimento)
		except ContasAReceber.DoesNotExist as erro:
			return HttpResponseNotFound("Conta não encontrada.")
		except ValueError as erro:
			return HttpResponseNotFound("Conta não encontrada.")

		if(conta.user != user):
			return HttpResponseForbidden("Alteração não permitida.")

		conta.delete()
			
		messages.success(request, "Conta " + conta.descricao + " excluída com sucesso!")
		return HttpResponseRedirect(reverse('contas_a_receber:index'))
	
	messages.warning(request, "Solicitação inválida.")
	return HttpResponseRedirect(reverse('contas_a_receber:index'))

@login_required
def recebimento(request):
	if(request.method == 'POST'):
		user 			= request.user
		tipoRecebimento = request.POST.get('banco')

		try:
			idConta 			= request.POST.get('id_contas_a_receber', 0)
			conta 				= ContasAReceber.objects.get(pk = idConta)
		except ContasAReceber.DoesNotExist as erro:
			return HttpResponseNotFound("Conta não encontrada.")
		except ValueError as erro:
			return HttpResponseNotFound("Conta não encontrada.")

		try:
			dt_recebimento = datetime.datetime.strptime(request.POST.get('data_recebimento'), "%Y-%m-%d")
		except ValueError as erro:
			return HttpResponseForbidden("Formato de data inválido.")

		if(conta.user != user):
			return HttpResponseForbidden("Recebimento não permitido.")
		
		conta.data_recebimento = dt_recebimento

		if(tipoRecebimento == ""):
			saldoCaixa 					= SaldoCaixa.objects.get(user = user)
			saldoCaixa.saldoAnterior 	= saldoCaixa.saldoAtual

			conta.tipo_conta = "c"

			caixa 					= LancamentosCaixa()
			caixa.data 				= conta.data_recebimento
			caixa.categoria 		= conta.categoria
			caixa.descricao 		= conta.descricao
			caixa. valor 			= conta.valor
			caixa.user 				= request.user
			caixa.conta_a_receber 	= conta

			saldoCaixa.saldoAtual += caixa.valor
			
			caixa.save()
			saldoCaixa.save()
	
		else:
			saldoBanco 					= SaldoBanco.objects.get(user = user)
			saldoBanco.saldoAnterior 	= saldoBanco.saldoAtual

			conta.tipo_conta = "b"

			try:
				agencia = ContaBanco.objects.get(pk = tipoRecebimento)
			except ContaBanco.DoesNotExist as erro:
				return HttpResponseNotFound("Agência não encontrada.")
			except ValueError as erro:
				return HttpResponseNotFound("Agência não encontrada.")

			if(agencia.user != user):
				return HttpResponseForbidden("Pagamento não permitido.")
				
			lancamento 					= LancamentosBanco()
			lancamento.banco 			= agencia
			lancamento.data 			= conta.data_recebimento
			lancamento.tipo 			= '1'
			lancamento.categoria 		= conta.categoria
			lancamento.descricao 		= conta.descricao
			lancamento. valor 			= conta.valor
			lancamento.user 			= request.user
			lancamento.conta_a_receber 	= conta
			
			agencia.saldo += lancamento.valor

			lancamento.save()
			agencia.save()

		conta.recebido = True
		conta.save()
		
		return HttpResponse("Recebimento efetuado com sucesso.")

@login_required
def cancelaRecebimento(request):
	if(request.method == 'POST'):
		user = request.user
		idRecebimento = request.POST.get('id_contas_a_receber', 0)

		try:
			conta = ContasAReceber.objects.get(pk = idRecebimento)
		except ContasAReceber.DoesNotExist as erro:
			return HttpResponseNotFound("Conta não encontrada.")
		except ValueError as erro:
			return HttpResponseNotFound("Conta não encontrada.")

		if(conta.user != user):
			return HttpResponseForbidden("Alteração não permitida.")

		if(conta.tipo_conta == "c"):
			lancamentoCaixa = LancamentosCaixa.objects.get(conta_a_receber = conta)
			lancamentoCaixa.delete()
			
			conta.recebido 			= False
			conta.tipo_conta 		= None
			conta.data_recebimento 	= None

			saldoCaixa 					= SaldoCaixa.objects.get(user = user)
			saldoCaixa.saldoAnterior 	= saldoCaixa.saldoAtual
			saldoCaixa.saldoAtual 		-= conta.valor
			saldoCaixa.save()
			conta.save()		
		else:
			lancamentoBanco = LancamentosBanco.objects.get(conta_a_receber = conta)

			try:
				agencia = ContaBanco.objects.get(pk = lancamentoBanco.banco.id)
			except ContaBanco.DoesNotExist as erro:
				return HttpResponseNotFound("Conta não encontrada.")
			except ValueError as erro:
				return HttpResponseNotFound("Conta não encontrada.")

			if(agencia.user != user):
				return HttpResponseForbidden("Pagamento não permitido.")

			conta.recebido 		= False
			conta.tipo_conta	= None
			agencia.saldo 		-= conta.valor
			
			agencia.save()
			lancamentoBanco.delete()
			conta.save()

		return HttpResponse('Recebimento cancelado com sucesso.')

@login_required
def filtrarContas(request):
	if(request.method == 'POST'):
		user = request.user

		try:
			mes = int(request.POST.get('mes'))
			ano = int(request.POST.get('ano'))
		except ValueError as erro:
			return HttpResponseForbidden("A data informada é inválida")
		status = request.POST.get('status', "")

		if(status not in ('abertas', 'recebidas', 'todas')):
			return HttpResponseForbidden("Status de conta é inválido.")		
		
		contas = ContasAReceber.getAccountsByStatusAndRangeOfDate(user, status, mes, ano)

		contasJson = serializers.serialize('json', contas, use_natural_foreign_keys=True, use_natural_primary_keys=True)
		return HttpResponse(contasJson, content_type="application/json")