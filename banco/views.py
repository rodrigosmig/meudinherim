from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from banco.models import ContaBanco, LancamentosBanco, SaldoBanco
from caixa.models import Categoria, SaldoCaixa
from banco.forms import ContaBancoForm, LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms
from usuario.models import UsuarioProfile
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import ProtectedError
import json
import datetime

@login_required
def cadastroBanco(request):
	user 			= request.user
	form_agencia 	= ContaBancoForm()

	if (request.method == 'POST'):
		form_agencia = ContaBancoForm(request.POST)
		
		if(form_agencia.is_valid()):
			bancos = form_agencia.save(commit = False)
			bancos.user = user 
			bancos.save()
			messages.success(request, 'Agência cadastrada com sucesso.')
			return HttpResponseRedirect(reverse('banco:agencia'))
		else:
			messages.warning(request, "Formulário inválido")

	template 		= 'banco/agencia.html'
	agencias 		= ContaBanco.objects.filter(user = user).exclude(tipo = ContaBanco.CARTAO_DE_CREDITO)
	credito			= ContaBanco.objects.filter(user = user).filter(tipo = ContaBanco.CARTAO_DE_CREDITO)
	contexto 		= {'form': form_agencia, 'agencias': agencias, 'credito': credito}

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	userProfile = UsuarioProfile.objects.get(user = user)
	contexto['profile'] = userProfile

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

	return render(request, template, contexto)

@login_required
def banco(request):
	#usuario logado
	user = request.user

	if(request.method == 'POST'):

		agencia = request.POST.get('agencia')
		mes = request.POST.get('mes')
		ano = request.POST.get('ano')

		agencia = ContaBanco.objects.get(pk = agencia)

		lancamentos = LancamentosBanco.objects.filter(data__month = mes).filter(data__year = ano).filter(user = user).filter(banco = agencia)
		
		lancJson = serializers.serialize('json', lancamentos, use_natural_foreign_keys=True, use_natural_primary_keys=True)

		return HttpResponse(lancJson, content_type="application/json")

	template = 'banco/banco.html'
	contexto = {}

	listAgencias = []
	todasAgencias = ContaBanco.objects.filter(user = user).exclude(tipo = ContaBanco.CARTAO_DE_CREDITO)

	for a in todasAgencias:
		id = a.id
		nome = a.banco
		saldo = str(a.saldo)
		listAgencias.append((id, nome, saldo))


	listAgencias = [{'id': id, 'agencia': agencia, 'saldo': saldo} for id, agencia, saldo in listAgencias]
	listAgencias = json.dumps(listAgencias, ensure_ascii=False)
	contexto['selectAgencias'] = listAgencias

	listCredito = []
	todasCredito = ContaBanco.objects.filter(user = user).filter(tipo = ContaBanco.CARTAO_DE_CREDITO)

	for c in todasCredito:
		id = c.id
		nome = c.banco
		saldo = str(c.saldo)
		listCredito.append((id, nome, saldo))


	listCredito = [{'id': id, 'agencia': credito, 'saldo': saldo} for id, credito, saldo in listCredito]
	listCredito = json.dumps(listCredito, ensure_ascii=False)
	contexto['selectCredito'] = listCredito

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

	userProfile = UsuarioProfile.objects.get(user = user)
	contexto['profile'] = userProfile	

	#para saldo da carteira
	saldoC = SaldoCaixa.objects.get(user = user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
	contexto['agencias'] = agencias	

	return render(request, template, contexto)

@login_required
def addLancamento(request):
	if(request.method == 'POST'):
		
		form = LancamentosBancoForm(request.POST)
		agencia = request.POST.get('banco')
		
		if(form.is_valid()):
			lancamento = form.save(commit = False)

			conta = ContaBanco.objects.get(pk = agencia)

			if (lancamento.tipo == "1"):				
				conta.saldo += lancamento.valor
			else:
				conta.saldo -= lancamento.valor

			conta.save()

			#relacionao o usuario logado com o lançamento
			lancamento.user = request.user
			lancamento.save()
			return HttpResponse('Lançamento efetuado com sucesso.')
	return HttpResponseServerError('Lançamento inválido')

@login_required
def editLancamento(request):

	if(request.method == 'POST'):

		id_user = request.user.id

		agencia = request.POST.get('banco')

		#id do lancamento clicado
		idLancamento = request.POST.get('id')
		#busca o lancamento a ser alterado
		lancamento = LancamentosBanco.objects.get(pk = idLancamento)
		#atribui o lancamento ao form	
		form = LancamentosBancoForm(request.POST, instance = lancamento)

		if(form.is_valid()):			
			form.save()
			conta = ContaBanco.objects.get(pk = agencia)
			lancamentos = LancamentosBanco.objects.filter(user_id = id_user).filter(banco = agencia)
			saldo = 0

			for l in lancamentos:
				if (l.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor			
			conta.saldo = saldo 

			conta.save()			

			return HttpResponse("Lançamento alterado com sucesso")
		else:
			return HttpResponseServerError("Formulário inválido")

	#id do lancamento clicado
	idLancamento = request.GET.get('id')
	lancamento = LancamentosBanco.objects.get(pk = idLancamento)	

	form = LancamentosBancoForm(instance = lancamento)
	form.getEditLancamentoForm(request)	

	if(lancamento.conta_a_pagar != None):
		contaID = "<div id='status_conta'>Pago</div>"
	elif(lancamento.conta_a_receber != None):
		contaID = "<div id='status_conta'>Recebido</div>"
	else:
		contaID = "<div id='status_conta'>Nenhum</div>"

	#retorna o id do lancamento junto com o formulario
	divId = "<div id='id_lancamento'>" + idLancamento + "</div>"

	form_html = {form.as_p(), divId, contaID}
	return HttpResponse(form_html)

@login_required
def delLancamento(request):

	if(request.method == 'POST'):
		
		id_user = request.user.id

		#id do lancamento a ser deletado
		idLancamento = request.POST.get('id')

		#busca o lançamento
		lancamento = LancamentosBanco.objects.get(pk = idLancamento)

		if(request.user.id == lancamento.user_id):
			lancamento.delete()

			agencia = request.POST.get('banco')
			conta = ContaBanco.objects.get(pk = agencia)
			lancamentos = LancamentosBanco.objects.filter(user_id = id_user).filter(banco = agencia)
			saldo = 0

			for l in lancamentos:
				
				if (l.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor			
			conta.saldo = saldo 

			conta.save()

			return HttpResponse("Lançamento excluído com sucesso.")
		else:
			return HttpResponseServerError("Lançamento não encontrado.")
		

	return HttpResponseServerError("Lançamento não encontrado.")

@login_required
def editAgencia(request):
	usuario = request.user 

	if(request.method == 'POST'):
		idAgencia = request.POST.get('id')

		try:
			agencia = ContaBanco.objects.get(pk = idAgencia)
		except ContaBanco.DoesNotExist as erro:
			messages.warning(request, "Agência não encontrada")
			return HttpResponseRedirect(reverse('banco:agencia'))

		form = ContaBancoForm(request.POST,instance = agencia)

		if (form.is_valid() and agencia.user == usuario):
			form.save()
			messages.success(request, "Agência alterada com sucesso")
			return HttpResponseRedirect(reverse('banco:agencia'))
		else:
			messages.warning(request, "Agência inválida")
			return HttpResponseRedirect(reverse('banco:agencia'))

	idAgencia = request.GET.get('idAgencia')
	
	try:
		agencia = ContaBanco.objects.get(pk = idAgencia)
	except ContaBanco.DoesNotExist as a:
		return HttpResponseNotFound()
	
	form = ContaBancoForm(instance = agencia)
	form.getEditBancoForm()	
	
	temp = 'id_agencia-alter_agencia'
	#retorna o id do agencia junto com o formulario
	divId = "<div id=temp>" + idAgencia + "</div>"
	form_html = {form.as_p(), divId}
	return HttpResponse(form_html)

@login_required
def delAgencia(request):
	if (request.method == 'POST'):		
		user 		= request.user
		idAgencia 	=  request.POST.get('id')

		try:
			agencia = ContaBanco.objects.get(pk = idAgencia)
		except ContaBanco.DoesNotExist as a:
			messages.warning(request, "Agência não encontrada")
			return HttpResponseRedirect(reverse('banco:agencia'))

		if(user == agencia.user):
			try:
				agencia.delete()
			except ProtectedError as erro:
				messages.error(request, "Não é possível excluir uma agencia/cartão que possua algum lançamento!")
				return HttpResponseRedirect(reverse('banco:agencia'))			
			
			messages.success(request, "Agência excluída com sucesso")
			return HttpResponseRedirect(reverse('banco:agencia'))
		else:
			messages.warning(request, "Agência inválida")
			return HttpResponseRedirect(reverse('banco:agencia'))

@login_required
def verificarContas(request):
	if(request.method == 'POST'):
		idLancamentoBanco = request.POST.get('id')
		lancamento = LancamentosBanco.objects.get(pk = idLancamentoBanco)
		if(lancamento.conta_a_pagar != None):
			return HttpResponseServerError('Lançamento realizado pelo contas a pagar. Para excluir este lançamento, cancele seu pagamento em Contas a Pagar.')
		elif(lancamento.conta_a_receber != None):
			return HttpResponseServerError('Lançamento realizado pelo contas a receber. Para excluir este lançamento, cancele seu recebimento em Contas a Receber.')
		else:
			return HttpResponse(idLancamentoBanco)

	else:
		HttpResponseServerError("Conta inexistente")

@login_required
def getAgencias(request):
	user = request.user
	agencias = ContaBanco.objects.filter(user = user).exclude(tipo = ContaBanco.CARTAO_DE_CREDITO)

	agenciasJson = serializers.serialize('json', agencias, use_natural_foreign_keys=True, use_natural_primary_keys=True)
	
	return HttpResponse(agenciasJson, content_type="application/json")

@login_required
def getCartao_Credito(request):
	user = request.user
	agencias = ContaBanco.objects.filter(user = user).filter(tipo = ContaBanco.CARTAO_DE_CREDITO)

	agenciasJson = serializers.serialize('json', agencias, use_natural_foreign_keys=True, use_natural_primary_keys=True)
	
	return HttpResponse(agenciasJson, content_type="application/json")


@login_required
def transferenciaEntreContas(request):
	if(request.method == 'POST'):
		user = request.user
		id_agencia_origem = request.POST.get('agencia_origem')
		id_agencia_destino = request.POST.get('agencia_destino')
		id_categoria_origem = request.POST.get('categoria_origem')
		id_categoria_destino = request.POST.get('categoria_destino')
		descricao = request.POST.get("descricao")
		data = request.POST.get('data')

		valor = float(request.POST.get('valor'))
		url = request.POST.get('url')

		if(descricao == ""):
			messages.warning(request, "A transferência deve ter uma descrição.")		
			return HttpResponseRedirect(url)

		try:
			data_lancamento = datetime.datetime.strptime(data, '%d/%m/%Y')
		except ValueError as error:
			messages.warning(request, "Data inválida. A data deve estar no formato DD/MM/AAAA")		
			return HttpResponseRedirect(url)

		if(not (id_agencia_origem.isnumeric() and id_agencia_destino.isnumeric())):
			messages.warning(request, "Agência inválida!")		
			return HttpResponseRedirect(url)

		if(not (id_categoria_origem.isnumeric() and id_categoria_destino.isnumeric())):
			messages.warning(request, "Categoria inválida!")		
			return HttpResponseRedirect(url)

		categoria_origem = Categoria.objects.get(pk = id_categoria_origem)
		categoria_destino = Categoria.objects.get(pk = id_categoria_destino)

		agencia_origem = ContaBanco.objects.get(pk = id_agencia_origem)
		agencia_destino = ContaBanco.objects.get(pk = id_agencia_destino)

		if(categoria_origem.user != user):
			messages.warning(request, "A categoria de origem é inválida.")
			return HttpResponseRedirect(url)
		
		if(categoria_destino.user != user):
			messages.warning(request, "A categoria de destino é inválida.")
			return HttpResponseRedirect(url)

		if(agencia_origem.user != user):
			messages.warning(request, "A agência origem é inválida.")
			return HttpResponseRedirect(url)
		
		if(agencia_destino.user != user):
			messages.warning(request, "A agência destino é inválida.")
			return HttpResponseRedirect(url)
		
		if(agencia_origem == agencia_destino):
			messages.warning(request, "As agências não podem ser iguais.")
			return HttpResponseRedirect(url)

		agencia_origem.adicionaLancamento(descricao, categoria_origem, data_lancamento, valor)
		agencia_destino.adicionaLancamento(descricao, categoria_destino, data_lancamento, valor)

		messages.success(request, "Transferência realizada com sucesso")
	
		return HttpResponseRedirect(url)

@login_required
def saqueBancario(request):
	if(request.method == 'POST'):
		user = request.user
		id_agencia = request.POST.get('agencia_saque')
		id_categoria_entrada = request.POST.get('categoria_entrada')
		id_categoria_saida = request.POST.get('categoria_saida')
		descricao = request.POST.get("descricao")
		data = request.POST.get('data')
		valor = float(request.POST.get('valor'))
		url = request.POST.get('url')

		if(descricao == ""):
			messages.warning(request, "A transferência deve ter uma descrição.")		
			return HttpResponseRedirect(url)

		try:
			data_lancamento = datetime.datetime.strptime(data, '%d/%m/%Y')
		except ValueError as error:
			messages.warning(request, "Data inválida. A data deve estar no formato DD/MM/AAAA")		
			return HttpResponseRedirect(url)

		if(not (id_agencia.isnumeric())):
			messages.warning(request, "Agência inválida!")		
			return HttpResponseRedirect(url)

		if(not (id_categoria_entrada.isnumeric() and id_categoria_saida.isnumeric())):
			messages.warning(request, "Categoria inválida!")		
			return HttpResponseRedirect(url)

		categoria_entrada = Categoria.objects.get(pk = id_categoria_entrada)
		categoria_saida = Categoria.objects.get(pk = id_categoria_saida)

		agencia = ContaBanco.objects.get(pk = id_agencia)

		if(categoria_entrada.user != user):
			messages.warning(request, "A categoria de entrada é inválida.")
			return HttpResponseRedirect(url)
		
		if(categoria_saida.user != user):
			messages.warning(request, "A categoria de saida é inválida.")
			return HttpResponseRedirect(url)

		if(agencia.user != user):
			messages.warning(request, "A agência origem é inválida.")
			return HttpResponseRedirect(url)

		agencia.saqueBancario(descricao, categoria_entrada, categoria_saida, data_lancamento, valor)
		
		messages.success(request, "Saque realizado com sucesso")
	
		return HttpResponseRedirect(url)
	