from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from caixa.models import LancamentosCaixa, Categoria, SaldoCaixa
from banco.models import SaldoBanco, ContaBanco
from caixa.forms import CategoriaForm, LancamentosForm
from banco.forms import LancamentosBancoForm
from django.http import JsonResponse
from django import forms
from datetime import datetime
from django.core import serializers
import json
from usuario.models import UsuarioProfile
from django.contrib import messages
from django.db.models import ProtectedError

@login_required
def lancamentos(request):
	#id do usuario logado
	id_user = request.user.id

	if(request.method == 'POST'):
		mes = request.POST.get('mes')
		ano = request.POST.get('ano')

		lancamentos = LancamentosCaixa.objects.filter(data__month = mes).filter(data__year = ano).filter(user_id = id_user)
		
		if(len(lancamentos) != 0):
			lancJson = serializers.serialize('json', lancamentos, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			return HttpResponse(lancJson, content_type="application/json")
		else:
			return HttpResponseServerError("Nenhum lançamento foi encontrado.")

	#armazena a data atual
	hoje = datetime.today()
	saldo = 0	
	template = 'caixa/caixa.html'
	
	#seleciona os lancamentos do mes atual
	lancamentos = LancamentosCaixa.objects.filter(data__month = hoje.month).filter(data__year = hoje.year).filter(user_id = id_user)
	
	contexto = {'lancamentos': lancamentos}
  	
  	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = request.user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = request.user)
	contexto['agencias'] = agencias

	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'].choices = separarCategorias(request)
	
	formBanco = LancamentosBancoForm()
	#Seleciona apenas o banco do usuario para o formulario
	formBanco.fields['banco'] = forms.ModelChoiceField(
		queryset = ContaBanco.objects.filter(user_id = request.user.id),
		empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
	)
	#seleciona apenas as categorias do usuario logado
	formBanco.fields['categoria'].choices = separarCategorias(request)

	#para adicionar lancamento
	contexto['formLancCaixa'] = formCaixa
	contexto['formLancBanco'] = formBanco

	userProfile = UsuarioProfile.objects.get(user = request.user)
	contexto['profile'] = userProfile

	return render(request, template, contexto)

@login_required
def categoria(request):
	form = CategoriaForm()

	if(request.method == 'POST'):
		if(request.POST.get('alterar')):
			idCategoria = request.POST.get('id_categoria')
			categoria = Categoria.objects.get(pk = idCategoria)
			form = CategoriaForm(request.POST, instance = categoria)
			if(form.is_valid()):
				form.save()
				messages.success(request, "Categoria " + categoria.descricao + " alterada com sucesso!")
		elif(request.POST.get('excluir')):
			idCategoria = request.POST.get('id_categoria')
			categoria = Categoria.objects.get(pk = idCategoria)		
			if(request.user == categoria.user):
				try:
					categoria.delete()
					messages.success(request, "Categoria " + categoria.descricao + " excluída com sucesso!")
				except ProtectedError as exception:
					messages.error(request, "Não é possível excluir uma categoria relacionada a um laçamento!")
					print(messages)
				
		else:
			form = CategoriaForm(request.POST)
			if(form.is_valid()):
				categoria = form.save(commit = False)
				categoria.user = request.user
				categoria.save()
				messages.success(request, "Categoria " + categoria.descricao + " adicionada com sucesso!")

	user = request.user
	template = 'caixa/categoria.html'
	catEntrada = Categoria.objects.filter(tipo = 1).filter(user = user)
	catSaida = Categoria.objects.filter(tipo = 2).filter(user = user)

	contexto = {'catEntrada': catEntrada, 'catSaida': catSaida, 'form': form}

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
	contexto['agencias'] = agencias

	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'].choices = separarCategorias(request)
	
	formBanco = LancamentosBancoForm()
	#Seleciona apenas o banco do usuario para o formulario
	formBanco.fields['banco'] = forms.ModelChoiceField(
		queryset = ContaBanco.objects.filter(user = user),
		empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
	)
	#seleciona apenas as categorias do usuario logado
	formBanco.fields['categoria'].choices = separarCategorias(request)

	#para adicionar lancamento
	contexto['formLancCaixa'] = formCaixa
	contexto['formLancBanco'] = formBanco

	userProfile = UsuarioProfile.objects.get(user = user)
	contexto['profile'] = userProfile

	return render(request, template, contexto)

@login_required
def editCategoria(request):
	user = request.user

	if(request.method == 'POST'):
		idCategoria = request.POST.get('id')
		categoria = Categoria.objects.get(pk = idCategoria)
		form = CategoriaForm(request.POST, instance = categoria)

		if(form.is_valid()):
			form.save()
			return HttpResponse('Categoria alterada com sucesso.')
		else:
			return HttpResponseServerError("Dados inválidos.")

	#id do lancamento clicado
	idCategoria = request.GET.get('id')

	lancamento = Categoria.objects.get(pk = idCategoria)

	form = CategoriaForm(instance = lancamento)

	form.fields['tipo'] = forms.ChoiceField(
        widget = forms.Select(
            attrs = {'class': 'form-control', 'id': 'id_tipo-alter_categoria'}
        ),
        choices = Categoria.TIPOS
    )
	
	form.fields['descricao'] = forms.CharField(
        label = 'Descrição',
        max_length = 32,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'id_descricao-alter_categoria', 'placeholder': 'Descreva a categoria'}
        )
    )

	#retorna o id da categoria junto com o formulario
	divId = "<div id='id-alter_categoria'>" + idCategoria + "</div>"

	form_html = {form.as_p(), divId}
	return HttpResponse(form_html)

@login_required
def delCategoria(request):
	if(request.method == 'POST'):
		#usuario logado
		user = request.user
		#id do lancamento a ser deletado
		idCategoria = request.POST.get('id')

		#busca a Categoria
		categoria = Categoria.objects.get(pk = idCategoria)		
		
		if(user == categoria.user):
			categoria.delete()
			
			return HttpResponse("Categoria excluída com sucesso")
		else:
			return HttpResponseServerError("Categoria não encontrado.")		

	return HttpResponseServerError("Conta não encontrado.")

@login_required
def addLancamento(request):
	if(request.method == 'POST'):	
		form = LancamentosForm(request.POST)
		if(form.is_valid()):
			lancamento = form.save(commit = False)

			#busca o saldo do usuario logado
			saldo = SaldoCaixa.objects.get(user = request.user)
			#atribui o valor do saldo anterior
			saldo.saldoAnterior = saldo.saldoAtual

			#atribui o novo saldo de acordo com a categoria do lançamento
			if(lancamento.categoria.tipo == "1"):
				saldo.saldoAtual += lancamento.valor
			else:
				saldo.saldoAtual -= lancamento.valor
			
			#salva o novo saldo
			saldo.save()

			#relacionao o usuario logado com o lançamento
			lancamento.user = request.user
			lancamento.save()
			return HttpResponse('Lançamento efetuado com sucesso.')
	
	return ('Lançamento inválido')

@login_required
def editLancamento(request):

	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id
		#id do lancamento clicado
		idLancamento = request.POST.get('id')
		#busca o lancamento a ser alterado
		lancamento = LancamentosCaixa.objects.get(pk = idLancamento)
		
		#atribui o lancamento ao form	
		form = LancamentosForm(request.POST, instance = lancamento)
		
		if(form.is_valid()):
			form.save()

			#busca o saldo do usuario logado
			saldoCaixa = SaldoCaixa.objects.get(user = request.user)
			lancamentos = LancamentosCaixa.objects.filter(user_id = id_user)
			saldo = 0
			
			for l in lancamentos:
				if (l.categoria.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor

								
			saldoCaixa.saldoAtual = saldo
			saldoCaixa.save()

			return HttpResponse("Lançamento alterado com sucesso")
		else:
			return HttpResponseServerError("Formulário inválido")

	#id do lancamento clicado
	idLancamento = request.GET.get('id')
	lancamento = LancamentosCaixa.objects.get(pk = idLancamento)
	form = LancamentosForm(instance = lancamento)

	#seleciona apenas as categorias do usuario logado
	form.fields['categoria'].choices = separarCategorias(request)

	form.fields['descricao'] = forms.CharField(
        label = 'Descrição',
        max_length = 32,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Descreva a transação', 'id': 'id_descricao-alter_caixa'}
        )
    )

	form.fields['valor'] = forms.DecimalField(
		label = 'Valor',
		min_value = 0.01,
		max_value = 9999.99,
		required = True,
		widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'id': 'id_valor-alter_caixa'}
        )
    )

	form.fields['data'] = forms.DateField(
        label = 'Data',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'id': 'datepicker-alter_caixa'}
        )
    )
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
		#id do usuario
		id_user = request.user.id
		#id do lancamento a ser deletado
		idLancamento = request.POST.get('id')

		#busca o lançamento
		lancamento = LancamentosCaixa.objects.get(pk = idLancamento)		
		
		if(request.user.id == lancamento.user_id):
			lancamento.delete()
			#busca o saldo do usuario logado
			saldoCaixa = SaldoCaixa.objects.get(user = request.user)
			lancamentos = LancamentosCaixa.objects.filter(user_id = id_user)
			saldo = 0
			
			for l in lancamentos:
				if (l.categoria.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor
								
			saldoCaixa.saldoAtual = saldo
			saldoCaixa.save()

			return HttpResponse("Lançamento excluído com sucesso")
		else:
			return HttpResponse("Lançamento não encontrado.")
		

	return HttpResponse("Lançamento não encontrado.")

@login_required
def verificarContas(request):
	if(request.method == 'POST'):
		idLancamentoCaixa = request.POST.get('id')
		lancamento = LancamentosCaixa.objects.get(pk = idLancamentoCaixa)
		if(lancamento.conta_a_pagar != None):
			return HttpResponseServerError('Lançamento realizado pelo contas a pagar. Para excluir este lançamento, cancele seu pagamento em Contas a Pagar.')
		elif(lancamento.conta_a_receber != None):
			return HttpResponseServerError('Lançamento realizado pelo contas a receber. Para excluir este lançamento, cancele seu recebimento em Contas a Receber.')
		else:
			return HttpResponse(idLancamentoCaixa)
	else:
		HttpResponseServerError("Conta inexistente")

#Para separar as categorias no template
def separarCategorias(request):
    user = request.user
    categorias = []
    entrada = []
    saida = []
    for categoria in Categoria.objects.filter(tipo = '1').filter(user = user).order_by('descricao'):
        entrada.append([categoria.id, categoria.descricao])

    for categoria in Categoria.objects.filter(tipo = '2').filter(user = user).order_by('descricao'):
        saida.append([categoria.id, categoria.descricao])

    categorias.append(['Entradas', entrada])
    categorias.append(['Saídas', saida])

    return categorias